from urllib.parse import urlencode

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Count, Case, When, F, DecimalField
from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from core.models import TxType, Category, SubCategory, Status
from cashflow.models import CashFlowEntry

def home(request):
    return redirect('entries_list')


def _base_context():
    return {
        'types': TxType.objects.order_by('name'),
        'statuses': Status.objects.order_by('name'),
    }


def _apply_filters(request, qs):
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    d_from = request.GET.get('date_from')
    d_to = request.GET.get('date_to')

    if status_id:
        qs = qs.filter(status_id=status_id)
    if type_id:
        qs = qs.filter(type_id=type_id)
    if category_id:
        qs = qs.filter(category_id=category_id)
    if subcategory_id:
        qs = qs.filter(subcategory_id=subcategory_id)
    if d_from:
        df = parse_date(d_from)
        if df:
            qs = qs.filter(created_at__gte=df)
    if d_to:
        dt = parse_date(d_to)
        if dt:
            qs = qs.filter(created_at__lte=dt)
    return qs


@require_GET
def entries_list(request):
    qs = CashFlowEntry.objects.select_related(
        'status', 'type', 'category', 'subcategory'
    ).order_by('-created_at', '-id')
    qs = _apply_filters(request, qs)

    # Итоги по фильтру (наименования типов могут отличаться, подставлены 'Пополнение' и 'Списание')
    INCOME_NAMES = ['Пополнение']
    EXPENSE_NAMES = ['Списание']
    totals = qs.aggregate(
        income=Sum(Case(When(type__name__in=INCOME_NAMES, then=F('amount')), default=0, output_field=DecimalField())),
        expense=Sum(Case(When(type__name__in=EXPENSE_NAMES, then=F('amount')), default=0, output_field=DecimalField())),
        cnt=Count('id'),
    )
    income = totals['income'] or 0
    expense = totals['expense'] or 0
    net = income - expense

    # Пагинация
    page = request.GET.get('page', 1)
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(page)

    # Базовый querystring без page
    params = request.GET.copy()
    params.pop('page', None)
    base_qs = params.urlencode()

    ctx = _base_context()
    ctx.update({
        'entries': page_obj.object_list,
        'page_obj': page_obj,
        'filters': request.GET.dict(),
        'base_qs': base_qs,
        'summary': {'income': income, 'expense': expense, 'net': net, 'cnt': totals['cnt']},
    })
    return render(request, 'ui/entries_list.html', ctx)


@require_http_methods(['GET', 'POST'])
def entry_create(request):
    ctx = _base_context()
    if request.method == 'POST':
        data = request.POST
        entry = CashFlowEntry(
            created_at=data.get('created_at') or None,
            status_id=data.get('status') or None,
            type_id=data.get('type') or None,
            category_id=data.get('category') or None,
            subcategory_id=data.get('subcategory') or None,
            amount=data.get('amount') or None,
            comment=(data.get('comment') or '').strip(),
        )
        try:
            entry.full_clean()
            entry.save()
            messages.success(request, 'Запись успешно создана.')
            return redirect('entries_list')
        except Exception as e:
            messages.error(request, f'Ошибка сохранения: {e}')
            ctx['form_data'] = data
    return render(request, 'ui/entry_form.html', ctx)


@require_http_methods(['GET', 'POST'])
def entry_edit(request, pk: int):
    entry = get_object_or_404(CashFlowEntry, pk=pk)
    ctx = _base_context()
    if request.method == 'POST':
        data = request.POST
        entry.created_at = data.get('created_at') or entry.created_at
        entry.status_id = data.get('status') or None
        entry.type_id = data.get('type') or None
        entry.category_id = data.get('category') or None
        entry.subcategory_id = data.get('subcategory') or None
        entry.amount = data.get('amount') or None
        entry.comment = (data.get('comment') or '').strip()
        try:
            entry.full_clean()
            entry.save()
            messages.success(request, 'Запись обновлена.')
            return redirect('entries_list')
        except Exception as e:
            messages.error(request, f'Ошибка обновления: {e}')
    ctx['entry'] = entry
    return render(request, 'ui/entry_form.html', ctx)


@require_POST
def entry_delete(request, pk: int):
    CashFlowEntry.objects.filter(pk=pk).delete()
    messages.success(request, 'Запись удалена.')
    return HttpResponseRedirect(reverse('entries_list'))


@require_POST
def entry_duplicate(request, pk: int):
    obj = get_object_or_404(CashFlowEntry, pk=pk)
    obj.pk = None
    obj.save()
    messages.success(request, 'Запись продублирована.')
    return HttpResponseRedirect(reverse('entries_list'))


@require_GET
def categories_options(request):
    type_id = request.GET.get('type')
    qs = Category.objects.filter(type_id=type_id).order_by('name') if type_id else Category.objects.none()
    return render(request, 'ui/partials/category_options.html', {'categories': qs})


@require_GET
def subcategories_options(request):
    category_id = request.GET.get('category')
    qs = SubCategory.objects.filter(category_id=category_id).order_by('name') if category_id else SubCategory.objects.none()
    return render(request, 'ui/partials/subcategory_options.html', {'subcategories': qs})


@require_GET
def entries_export_csv(request):
    qs = CashFlowEntry.objects.select_related(
        'status', 'type', 'category', 'subcategory'
    ).order_by('-created_at', '-id')
    qs = _apply_filters(request, qs)

    def row_iter():
        yield ['date', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        for e in qs:
            yield [
                str(e.created_at),
                e.status.name, e.type.name,
                e.category.name, e.subcategory.name,
                f'{e.amount}', e.comment or ''
            ]

    def generate():
        for row in row_iter():
            escaped = []
            for cell in row:
                s = str(cell).replace('"', "''")
                escaped.append(f'"{s}"')
            yield (','.join(escaped) + '\n')

    resp = StreamingHttpResponse(generate(), content_type='text/csv; charset=utf-8')
    resp['Content-Disposition'] = 'attachment; filename="cashflow_export.csv"'
    return resp
