from a2a.types import AgentCard

from a2a_acl.interface.interface import SkillRequest
from a2a_acl.interface.card_conversion import bdi_card_from_a2a_card
from a2a_acl.a2a_utils.card_holder import CardHolder
from mistral_selector_prompt import ask_llm_for_agent_selection


class HotRepository:
    """A repository of running agents."""

    urls: set[str]
    cards: CardHolder

    def __init__(self):
        self.urls = set()
        self.card_holder = CardHolder()

    async def register(self, url):
        res = await self.card_holder.retrieve_card_from(url)
        if res:
            self.urls.add(
                url
            )  # append only if the card has been retrieved successfully
            print(url + " successfully registered")
        else:
            print("Error: did not manage to get card from " + url)

    def get_cards_by_skills(self, skills: list[SkillRequest]) -> list[AgentCard]:
        print(
            "Received the request to filter cards with following skills: " + str(skills)
        )
        return [
            card
            for card in self.card_holder.cards
            if bdi_card_from_a2a_card(card).has_declared_skills(skills)
        ]

    def get_top_card_by_skills(self, skills: list[SkillRequest]) -> AgentCard:
        cards = self.get_cards_by_skills(skills)
        if cards == []:
            return None
        selected_card = cards[0]
        selected_score = self.card_holder.get_reputation_by_card(selected_card)
        for c in cards:
            s = self.card_holder.get_reputation_by_card(c)
            if s > selected_score:
                selected_score = s
                selected_card = c
        return selected_card

    def select_by_llm(self, prompt: str, skills: list[SkillRequest]) -> AgentCard:
        cards = self.get_cards_by_skills(skills)
        if not cards == []:
            best_score = self.card_holder.get_reputation_by_card(cards[0])
            for c in cards:
                s = self.card_holder.get_reputation_by_card(c)
                if s > best_score:
                    best_score = s
            worse_score = self.card_holder.get_reputation_by_card(cards[0])
            for c in cards:
                s = self.card_holder.get_reputation_by_card(c)
                if s < worse_score:
                    worse_score = s

            def reputation(c):
                r = self.card_holder.get_reputation_by_card(c)
                if best_score == worse_score:
                    return "unknown"
                elif r == worse_score:
                    return "bad"
                elif r == best_score:
                    return "good"
                else:
                    return "neutral"

            annotated_cards = [(c, reputation(c)) for c in cards]
            i = ask_llm_for_agent_selection(prompt, annotated_cards)
            return cards[i]
        else:
            return None

    def print_state(self):
        print("Registered hot agents:")
        for url in self.urls:
            c = self.card_holder.get_card_by_url(url)
            n = c.name if c else "-"
            if n.endswith("\n"):
                n = n.removesuffix("\n")
            print(
                url
                + " ("
                + n
                + ", reputation= "
                + str(self.card_holder.get_reputation_by_url(url))
                + ", with "
                + str(len(c.skills))
                + " skill(s))"
            )
        print("(end)")

    def degrade(self, url: str):
        self.card_holder.degrade(url)
        print(
            "Degraded reputation of "
            + url
            + " to "
            + str(self.card_holder.get_reputation_by_url(url))
        )
