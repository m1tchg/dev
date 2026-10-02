I reworked a docs-as-code harness to mine better Japanese flash cards. A harness in a docs-as-code workflow might help an agent fill content gaps or add tags. Here, it's filling fields on a flash card to help me study Japanese.

## Design patterns reworked

Loop engineering design patterns map onto this project one to one:

- **Schema design**
  The schema tells the agent what done looks like. It's the contract.

- **Signal design**
  The agent proposes content edits based on an analytics signal. In docs as code, an agent might identify content gaps based on a signal like support ticket volume. 

  Analytics signals for flash cards look like a difficulty score, measuring how hard is it for me to consistently remember a card. These metrics come from the FSRS spaced repetition algorithm.

- **Loop architecture**
  The LLM self-corrects based on the FSRS performance data. The signal becomes the degradation condition of a feedback loop.

  The loop's stop condition is a re-measure step. The agent's only done when the signal says the edit worked.

- **Gate design**

  This project made it explicit that human gates can break. Since I'm still learning Japanese, I can't evaluate an edit. What form does the human gate take when the human can't verify the agent's work? 

  In docs-as-code workflows, gates are designed around the expectation that the human is the domain expert. Agent and human might drop into a maker/checker pattern.

  Wearing these n00b glasses, I learned to look for gate design patterns like how the gate degrades. The less domain knowledge the human has about the agent's output, the more the gate shifts from explicit to behavioral (the FSRS retrieval signal).
  
  Basically, the FSRS difficulty is the gate. When the FSRS difficulty for a batch, like the cards from an episode, stabilizes, then I'll do a Git merge that accepts or reject's the agent's edits in an asynchronous batch.


## Mining honorific shifts from real life

"What are you working on?" someone I just met at the Python meetup humbly inquires, selecting honorifics that lower themselves, gauging a polite distance. I grind out something from a neutral distance. There is no there there. "I'm working on my portfolio, freelancing gig to gig ..."

"Interesting!" She shifts into my register. Now we're in a groove coworkers might use.

"What are you working on?"

"I'm building out a content team to introduce our new automotive vision AI product." Now we're bubbling along as friends. Well, she is. I'm trapped inside my polite-as-neutral space suit.

We exchange business cards, each using humble language. There's a warmth to tracking the set phrases, stages together.

It's not a volitional, performative politeness. It's [*wakimae*](http://www.sachikoide.com/OntheNotionofWakimae.pdf), the act of selecting honorific grammatical forms (*keigo*) to establish Tachi-ichi (立ち位置), "where one stands."
To place yourself, you need to know the ground you're standing on, the axes along which you index your Tachi-ichi. 

Some textbooks boil it down to two, humble and honorific language. But you sound a little 2D when everyone else is cooking in five dimensions. Sachiko Ide enumerates the axes along which you assess your Tachi-ichi:

- Status
- Age
- Power
- Solidarity (familiarity)
- Formality (of occasion or topic)

## Mining flash cards from business manga

I leave the meetup early. It's night out. Akihabara seems suddenly deserted. Lost without a guide, I wander into a used bookstore, pick through bargain bins of manga, and uncover Ebisawa, the recruiter from *Angel Bank: Dragon Zakura Gaiden*, who coaches 32-year-old English teacher Ino Mamako through becoming a recruiter. A *keigo* shift master. "Let's go!" he seems to say.

## The first card

I buy a few missing volumes online, through Mercari. Chatting with the seller gives me my first keigo shift card. 

Mercari is Japan's homegrown Craigslist; it connects to Japanese banks and domestic shipping. It also channels sellers and buyers through a dialogue of *keigo* shifts at each step of the transaction. What you'd expect.

Buying the _Angel Bank_ volume starts the dialogue. The seller starts out formal, that is, humble. "I'd be grateful if you left a review."

I introduce myself with humble language that matches the distance, "Thanks for the shipping notification, I'll be sure to leave a review." 

"Don't mention it," the seller replies, in the same formal-humble register, the humble language you'd use with a client. "It helps a lot," she adds, but now in a neutral register that's less stiff. We're not suddenly close friends, in the same in-group. We're still _soto_, out-group. But, it's an expression of personal gratitude.

Boom. I recognize the shift, take some quick notes on what I can observe, then pass those to the agent to analyze the effect and generate a card.   

The agent also fills fields that don't go on the card but help it continuously improve.

## The schema

A two-level schema separates scene fields and card fields. Some of the schema structures the flash card, the fields that go on the front and back. Other fields don't go on the card but help the agent track the keigo analysis that drive its revisions.

Another way to slice the schema: The agent fills the analytical-level fields, and I just fill the observational fields. I can only verify fields at the observational level, since I only know the grammar of keigo; I'm still learning the analysis. 

The dataset looks like this.

``` json
{
  "scene_id": "mercari_chat1",
  "participants": {"B": "Buyer", "S": "Seller"},
  "setting": "Mercari chat after purchase, formal.",
  "cards": [
    {
      "card_id": "m1_c1_t1",
      "delta": "Buyer volunteers to leave a review. 発送のご連絡ありがとうございます。届きましたら受取評価をいたします。",
      "before": "Seller's request for a review: 到着しましたら、大変お手数ですが、受取評価して頂けますと助かります。よろしくお願いします。",
      "after": "Seller's thanks: とんでもございません。受取評価、助かります。引き続き、よろしくお願いします。",
      "axis": ["solidarity"],
      "form": "助かります",
      "function": "indexes distance reduced within soto register.",
      "mode": "indexical"
    }    
  ]
}
```

The agent fills `axis`, `form`, `function`, and `mode`.

## Priming your recognition for immersion learning

I'm learning keigo analysis from the agent as well as the cards. As I get better at recognizing the necessary `form` to fill the blank, my FSRS scores will improve. But I'm also reviewing the agent's proposed edits. As I read the agent's analysis, I'm priming my attention to recognize the parameters of re-indexing events at the next meetup.

You can learn everything you need from immersion, as Autumn Skerritt summarizes in her overview of the [JJ method](https://skerritt.blog/jj-method-for-japanese/). She adds that flash cards prime your brain to recognize forms during immersion. VanPatten, the linguist who co-created Structured Input, helped me thread these together: because you can pick up everything you need from context, your brain sees the morphemes you need to study as redundant with the context. So your brain ignores them.

In the Mercari example, the blank on the front of the card can only be filled by 助かります (Tasukarimasu, "It's helpful"), that specific verb, that specific masu form. ありがとうございます (Arigatou-gozaimasu, "Thank you very much"), no. 嬉しい (Hoshii, "I'd like that"), no.

Thankfully the agent is an expert Japanese linguist who can nail those cards-with-atomicity all day long.

We'll hook up the harness in part two. Check back in sometime.
