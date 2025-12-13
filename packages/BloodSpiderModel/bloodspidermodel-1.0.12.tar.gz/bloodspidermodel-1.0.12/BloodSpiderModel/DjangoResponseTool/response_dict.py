from django.http import JsonResponse

# django 分页
from django.core.paginator import Paginator

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_page(models_list, page_size=10, page_num=1):
    """
    对查询集进行分页处理并返回格式化的分页信息

    参数:
        models_list: Django查询集或列表，需要分页的数据
        page_size: 整数，每页显示的数据条数，默认10
        page_num: 整数，请求的页码，默认1

    返回:
        字典，包含分页相关信息和当前页数据
    """
    # 类型检查和处理
    try:
        page_size = int(page_size)
        page_num = int(page_num)
    except (ValueError, TypeError):
        page_size = 10
        page_num = 1

    # 确保page_size为正数
    page_size = max(1, page_size)

    paginator = Paginator(models_list, page_size)

    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        # 页码不是整数时返回第一页
        page = paginator.page(1)
    except EmptyPage:
        # 页码超出范围时返回最后一页
        page = paginator.page(paginator.num_pages)

    # 处理下一页和上一页可能不存在的情况
    next_page = page.next_page_number() if page.has_next() else None
    prev_page = page.previous_page_number() if page.has_previous() else None

    return {
        "page": {
            "count": paginator.count,  # 总数据条数
            "num_pages": paginator.num_pages,  # 总页数
            "object_list": page.object_list,  # 当前页数据
            "number": page.number,  # 当前页码
            "has_next": page.has_next(),  # 是否有下一页
            "has_previous": page.has_previous(),  # 是否有上一页
            "next_page_number": next_page,  # 下一页页码，不存在则为None
            "previous_page_number": prev_page,  # 上一页页码，不存在则为None
            "page_size": page_size  # 每页显示条数
        }
    }


def response_dict(code : int = 0, message : str = "", data : dict|list = None):
    return JsonResponse({
        "code": code,
        "message": message,
        "data": data,
    })

# 获取第一个错误信息
def get_first_error(form):
    first_error = next(iter(form.errors.items()))
    field_name, error_list = first_error
    error_msg = {
        field_name: error_list[0]
    }
    return error_msg