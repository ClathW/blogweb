from rest_framework.exceptions import ValidationError


def parse_pagination(query_params, default_page_size=10, max_page_size=100):
    """Return validated page and page_size integers from query params."""
    page = _parse_positive_int(query_params.get('page', 1), 'page')
    page_size = _parse_positive_int(query_params.get('page_size', default_page_size), 'page_size')

    if page_size > max_page_size:
        raise ValidationError({'page_size': f'page_size不能超过{max_page_size}'})

    return page, page_size


def paginate_queryset(queryset, page, page_size):
    total = queryset.count()
    total_pages = max(1, (total + page_size - 1) // page_size)
    start = (page - 1) * page_size
    end = start + page_size

    return queryset[start:end], {
        'count': total,
        'page': page,
        'page_size': page_size,
        'total_pages': total_pages,
    }


def _parse_positive_int(value, field_name):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        raise ValidationError({field_name: f'{field_name}必须是正整数'})

    if parsed < 1:
        raise ValidationError({field_name: f'{field_name}必须是正整数'})

    return parsed
