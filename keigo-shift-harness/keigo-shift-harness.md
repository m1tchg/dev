A harness in a docs-as-code workflow might help an agent add tags or suggest edits, like the [Hemingway app](https://hemingwayapp.com/). I reworked a docs-as-code agent harness to mine better Japanese flash cards. 

## Introducing the series

Read manga and write Python while you study Japanese:

- Learn _keigo_ by reading business manga. 
- Translate manga as you read with your phone and OCR tools.
- Find the right flash card tool for you, Anki, Obsidian, or Notion.
- Make effective flash cards.
- Build a harness for content governance.

I have to do the harness before the manga. But feel free to jump around the sections:

- [Keigo? Business manga?](#keigo-business-manga)
- [Design patterns reworked](#design%20patterns%20reworked)
- [Mining keigo shifts from real life](#mining%20keigo%20shifts%20from%20real%20life)
- [Mining flash cards from business manga](#mining%20flash%20cards%20from%20business%20manga)
- [The first card](#the%20first%20card)
- [The schema](#the%20schema)
- [Priming your recognition for immersion learning](#priming%20your%20recognition%20for%20immersion%20learning)

## Keigo? Business manga?

Keigo is the grammar that you use to speak with humility about yourself and honor others. Business manga explores workplace drama. It might inspire your investment strategy. Keigo shifts are part of the fun.

This article series uses *Angel Bank: Dragon Zakura Gaiden*. A recruiter named Ebisawa coaches his new hire, 32-year-old ex-English teacher Ino Mamako.

## Design patterns reworked

Loop engineering design patterns map onto this project one to one:

- **Schema design**
  The schema is the contract for the content that the agent should output.

- **Loop architecture**
  One loop iteration passes through signal → edit → gate → re-measure.

  The agent stops the loop when the signal says the edit worked.

- **Signal design**
  The agent proposes edits based on an analytics signal. In a docs-as-code environment, an agent might identify content gaps based on a signal like support ticket volume.

  The analytics signal for a flash card is the difficulty score. Is it hard for me to remember this card? This metric comes from the FSRS spaced repetition algorithm. The LLM self-corrects based on the FSRS performance data.

- **Gate design**
  I'm still learning keigo, so I can't evaluate an edit. What form does the human gate take when the human can't verify the agent's work?

## Mining keigo shifts from real life

"What are you working on?" she asks. We just met at a Python meetup. She gauges a polite distance, selecting humble language.

"I'm working on my portfolio, freelancing gig to gig ..." I grind out from a neutral distance. There is no there there.

"Interesting!" She shifts into my register. Now we're tracking a groove coworkers might use.

"What are you working on?"

"I'm building out a content team to introduce our new chip for automotive vision AI." Now we're bubbling along as friends. Well, she is. I'm trapped inside my polite-as-neutral space suit.

We exchange business cards, each using humble language. There's a warmth to tracking the set phrases, stages together.

It's not a volitional, performative politeness. It's [*wakimae*](http://www.sachikoide.com/OntheNotionofWakimae.pdf). Wakimae is a noun. You use it like, "That person has wakimae." It's the observance of social norms.

You can observe wakimae in how a speaker selects honorific grammar.
Some textbooks give you two levers: humble and honorific language. Up, down. But native speakers cook up, index, their sense of place in five-dimensional space.

Sachiko Ide lists the five axes:

- Status
- Age
- Power
- Solidarity/familiarity
- Formality of occasion or topic

## Mining flash cards from business manga

I leave the meetup early. It's night out. Akihabara is empty. I wander into a used bookstore. I pick through bargain bins of manga. Twenty minutes later, I pluck out the recruiters Ebisawa and Ino on the cover of *Angel Bank*.

## Mining the first card

I buy a few missing volumes online, through Mercari. Chatting with the seller gives me my first keigo shift card.

Mercari is Japan's homegrown Craigslist. Sellers and buyers wind through a dialogue of keigo shifts at each step of the transaction.

I introduce myself with humble language that matches the distance. "Thanks for the shipping notification. I'll be sure to leave a review."

"Don't mention it," the seller replies. She matches the humble language. You'd use this register when talking with a client. "It helps a lot," she adds. But she use a neutral register that's less stiff. We're still *soto*, out-group. But the shift leaves a wake that adds a dash of warmth. 

I take some quick notes on what I can observe, then pass those to the agent to analyze the mechanics I can't see.

## Designing the schema

There might be multiple shifts in the same scene. To reflect this, a two-level schema separates scene fields and card fields.

The cards are Cloze cards, where you fill in the blank. The front of the card shows the `before` and `after` sentences. I fill the blank in the `after` sentence with the keigo `form` that changed.

The agent identifies the `form`. It also fills the rest of the fields, like Ide's wakimae axes. These are the agent's notes. The agent uses these to self-correct.

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
      "form": "助かります",
      "axis": ["solidarity"],
      "function": "indexes distance reduced within soto register.",
      "mode": "indexical"
    }    
  ]
}
```

## Making flash cards that prepare you for immersion

You can learn everything you need from immersion. That's the theory of the JJ method. Autumn Skerritt [introduces](https://skerritt.blog/jj-method-for-japanese/) how to follow the JJ method to make better flash cards. She explains that flash cards prep your brain to recognize forms during immersion.

Bill VanPatten's [Input Processing theory](https://en.wikipedia.org/wiki/Input_Processing_theory) explains why you need to train your brain. Your brain ignores keigo forms because they're redundant with the context.

VanPatten's non-redundancy principle helps you write better flash cards. Remove hints from the front of the card so your brain can't cheat.

How do you make sure your flash cards drill on keigo and nothing else? We'll explore patterns that make good flash cards in a later article.
