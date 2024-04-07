from django.shortcuts import render


def about(request):

    context = {
        "key": 0,
    }
    return render(request, "home/about.html", context)


def shop(request):

    context = {
        "key": 0,
    }
    return render(request, "home/shop.html", context)


def workshop(request):

    context = {
        "key": 0,
    }
    return render(request, "home/workshop.html", context)
