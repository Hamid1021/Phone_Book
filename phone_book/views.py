from django.shortcuts import render, redirect
from django.template import loader
from django.http import JsonResponse
from phone_book.models import BookPhone, Book_User, BookOwner, Avatar


def profile(request):
    if not request.user.is_authenticated:
        return redirect("/")
    user = request.user
    book_owner = BookOwner.objects.filter(user=user).first()
    avatars = Avatar.objects.filter(
        status = True,
        is_deleted = False,
    )
    if request.POST:
        try:
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            avatar_id = int(request.POST.get("selectedAvatar"))
            avatar = Avatar.objects.filter(pk=avatar_id).first()
            user.first_name = first_name
            user.last_name = last_name
            book_owner.avatar = avatar
            user.save()
            book_owner.save()
        except:
            pass

    context = {
        "avatars":avatars,
        "object":book_owner,
        "book_owner":book_owner,
    }
    return render(request, "profile.html", context)


def phone_book_view(request):
    if not request.user.is_authenticated:
        return redirect("/")
    user = request.user
    book_owner = BookOwner.objects.filter(user=user).first()
    avatars = Avatar.objects.filter(
        status = True,
        is_deleted = False,
    )
    all_product = Book_User.objects.get_all_books_by_user_or_none(request.user)
    context = {
        "avatars":avatars,
        "book_owner":book_owner,
        "object_list":all_product,
    }
    return render(request, "contact_directory.html", context)


def get_all_contact(request):
    if request.user.is_anonymous:
        output_data = {
            'posts_html': None,
        }
        return output_data
    
    all_product = Book_User.objects.get_all_books_by_user_or_none(request.user)
    posts_html = loader.render_to_string(
        'AllContacts.html',
        {'object_list': all_product}
    )
    output_data = {
        'posts_html': posts_html,
    }
    return output_data


def add_phone_book(request):
    try:
        user = request.user
        book_owner = BookOwner.objects.filter(user=user).first()

        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        phone_number_1 = request.POST.get('phone_number_1')
        avatar_id = request.POST.get('avatar_id')
        post = request.POST.get('post')

        is_deleted = False

        avatar = Avatar.objects.filter(pk=avatar_id).first()

        book_phone, st = BookPhone.objects.get_or_create(
            name=name,
            last_name=last_name,
            phone_number=phone_number,
            phone_number_1=phone_number_1,
            avatar=avatar,
            post=post,
            is_deleted=is_deleted,
        )

        Book_User.objects.get_or_create(
            book_owner = book_owner,
            book_phone = book_phone,
            status = True,
            is_deleted = False,
        )

        status = True
    except:
        status = False
    posts_html = get_all_contact(request)["posts_html"]
    output_data = {
        'status': status,
        'posts_html': posts_html,
    }
    return JsonResponse(output_data)


def del_phone_book(request):
    try:
        user = request.user
        book_owner = BookOwner.objects.filter(user=user).first()

        try:
            el_id = int(request.POST.get('el_id'))
            book_user = Book_User.objects.get(
                pk=el_id, book_owner=book_owner, is_deleted=False, status=True
            )
            book_user.is_deleted = True
            book_user.save()

            status = True
        except:
            status = False
    except:
        status = False
    posts_html = get_all_contact(request)["posts_html"]
    output_data = {
        'status': status,
        'posts_html': posts_html,
    }
    return JsonResponse(output_data)


def search_phone_book(request):
    query = request.POST.get('query')
    all_product = Book_User.objects.get_all_books_by_user_or_none(request.user)
    all_product_filterd = Book_User.objects.get_all_product_filterd_or_none(request.user, query)
    if query is None:
        posts_html = loader.render_to_string(
            'AllContacts.html',
            {'object_list': all_product}
        )
    else:
        posts_html = loader.render_to_string(
            'AllContacts.html',
            {'object_list': all_product_filterd}
        )
    output_data = {
        'posts_html': posts_html,
    }
    return JsonResponse(output_data)
