import os

from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from sweetify import sweetify

from django_htmx.http import HttpResponseClientRedirect

from .models import *
from .forms import *


# Create your views here.

@login_required
def home(request):
    """
    Renders the home page for the logged-in user.

    Parameters:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.

    Raises:
        None
    """
    return render(request, "core/home.html",
                  {
                      "objects": PokerSession.objects.filter(participants__user=request.user),
                      "form": PokerSessionForm()
                  })


@require_POST
@login_required
def create_poker_session(request):
    """
    Creates a poker session.

    This function is responsible for creating a poker session based on the data provided in the request.
    It performs the following steps:
    1. Validates the data provided in the request.
    2. If the data is valid, it creates a new poker session with the current user as the owner.
    3. Generates the features for the created poker session.
    4. Creates a participant for the current user in the poker session.
    5. Displays a success or error message using sweetify.toast.
    6. Redirects the user to the home page.

    Parameters:
    - request: The HTTP request object containing the data for creating the poker session.

    Returns:
    - A redirect response to the home page.

    Raises:
    - N/A
    """
    form = PokerSessionForm(request.POST, request.FILES)
    if form.is_valid():
        form.instance.owner = request.user
        _poker_session = form.save()
        _poker_session.gen_features()
        Participant.objects.create(poker_session=_poker_session, user=request.user)
        sweetify.toast(request, "Partie de poker créée avec succès", icon="success", timer=3000)
    else:
        sweetify.toast(request, "Erreur lors de la création de la session", icon="error", timer=3000)
    return redirect("core:home")


def poker_session(request, pk):
    """
    Retrieves a poker session using the provided primary key and performs various operations on it.

    Args:
        request: The HTTP request object.
        pk: The primary key of the poker session to retrieve.

    Returns:
        A rendered HTML template with the poker session, its features, and participants.
    """
    poker_session = PokerSession.objects.get(pk=pk)
    participants = Participant.objects.filter(poker_session=poker_session)
    features = Feature.objects.filter(poker_session=poker_session)
    current_feature = poker_session.get_next_feature
    if current_feature:
        tour_nbr = Tour.objects.filter(feature=current_feature).count()
        # breakpoint()
        if poker_session.mode == "strict" or (
            poker_session.mode == "medium" and tour_nbr == 1):
            if current_feature.is_completed:
                if current_feature.is_consensus:
                    # breakpoint()
                    current_feature.voted = True
                    current_feature.story_points = current_feature.get_last_tour.votes.first().vote
                    current_feature.save()
                    sweetify.success(request, f"Consensus atteint pour la fonctionnalité {current_feature.title}",
                                     icon="success",
                                     timer=5000)
                else:
                    if poker_session.status != "finished":
                        current_feature.set_next_tour()
                        sweetify.warning(request, f"Consensus non atteint pour la fonctionnalité {current_feature.title}",
                                         icon="warning",
                                         timer=5000)
        elif tour_nbr > 1:
            if current_feature.is_completed:
                current_feature.voted = True
                current_feature.story_points = int(current_feature.get_last_tour.votes.aggregate(vote=Avg("vote")).get("vote"))
                current_feature.save()
    poker_session.update_status()
    if poker_session.status == "finished":
        # store the list of the features as a list of dictionaries in a file
        features_list = []
        for feature in features:
            feature_dict = {
                "title": feature.title,
                "description": feature.description,
                "difficulty": feature.story_points,
            }
            features_list.append(feature_dict)
        try:
            os.remove(f"planning_poker/media/backlogs/backlog_{poker_session.pk}.json")
        except Exception as e:
            pass
        try:
            with open(f"planning_poker/media/backlogs/backlog_{poker_session.pk}.json", "w") as f:
                json.dump(features_list, f)
            poker_session.result_file = f"planning_poker/media/backlogs/backlog_{poker_session.pk}.json"
            poker_session.save()
        except Exception as e:
            pass
        sweetify.success(request, f"Session de planning poker terminée", icon="success",
                         timer=5000)
    return render(request, "core/poker_session.html",
                  {"poker_session": poker_session, "features": features, "participants": participants})


@require_POST
def join_poker_session(request):
    """
    Join a poker session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: A redirect to the poker session page.
    """
    pk = request.POST.get("session_id")
    poker_session = get_object_or_404(PokerSession, pk=pk)
    participants = poker_session.participants.all()
    if participants.count() < poker_session.players:
        if request.user not in poker_session.participants.all():
            try:
                Participant.objects.create(poker_session=poker_session, user=request.user)
            except Exception as e:
                pass
            sweetify.success(request, f"Vous avez rejoint cette session de planning poker ", icon="success",
                   timer=5000)
    return redirect("core:poker_session", pk=poker_session.pk)


def vote(request, poker_session_id, card):
    """
    This function handles the voting process for a poker session feature.

    Parameters:
        request (HttpRequest): The HTTP request object.
        poker_session_id (int): The ID of the poker session.
        card (str): The card value representing the vote.

    Returns:
        HttpResponseRedirect: The redirect response to the poker session page.
    """
    # breakpoint()
    _pokersession = get_object_or_404(PokerSession, pk=poker_session_id)
    _feature = _pokersession.get_next_feature
    _participant = Participant.objects.get(poker_session=_pokersession, user=request.user)
    _tour = _feature.get_last_tour if _feature else None
    _cafe = card == "cafe"
    _interro = card == "interro"

    if _cafe or _interro:
        sweetify.warning(request, f"Exprimez vous dans le chat", icon="warning",
                         timer=5000)
        return redirect("core:poker_session", pk=poker_session_id)
    card = int(card)
    if _tour:
        if _tour.votes.filter(voter=_participant).exists():
            sweetify.error(request, f"Vous avez déjà voté pour cette fonctionnalité", icon="error", timer=5000)
            return redirect("core:poker_session", pk=poker_session_id)
        vote = Vote.objects.create(poker_session=_pokersession, feature=_feature, voter=_participant, vote=card, tour=_tour)
    else:
        _tour = Tour.objects.create(poker_session=_pokersession, feature=_feature, designation=1)
        Vote.objects.create(poker_session=_pokersession, feature=_feature, voter=_participant, vote=card, tour=_tour)
    sweetify.success(request, f"Votre vote a été pris en compte", icon="success", timer=5000)
    return redirect(reverse("core:poker_session", kwargs={"pk": poker_session_id}))
