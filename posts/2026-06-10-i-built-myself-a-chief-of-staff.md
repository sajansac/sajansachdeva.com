title: I Built Myself a Chief of Staff
dek: Markdown files, an OS timer, and an agent named Donna — and what it cost me to learn that guardrails are the product.
date: 2026-06-10
slug: i-built-myself-a-chief-of-staff
---

The most reliable colleague I have doesn't exist.

Her name is Donna — yes, from *Suits* — and every morning she emails me a brief. The three things that actually matter today. Two emails that need my eyes. What's been parked, and why. My calendar is already blocked, and every block carries the ID of the task it serves, so the day never needs re-deriving from memory. I read that brief the way heads of state read their morning intelligence digest: slowly, with coffee, before the world starts asking for things.

Donna is an AI agent. Under her sits a system I've built out of the most boring infrastructure I could find: plain Markdown files, an OS timer, and a strict constitution. This is the story of that system — how it's wired, why it's shaped like a brain, and the mistakes it made on my behalf before I understood where the hard limits had to go.

## The job is decisions, not admin

I'm a product manager at Amazon. The topics I deal with are complex and interlocking — a delivery-window question touches lead times, which touch capacity planning, which touches a chargeback policy owned by a team three orgs away. On a good day, my actual job is making a small number of high-quality decisions. On a normal day, that job arrives buried in admin: triaging email, filing notes, moving information between tools, reconstructing "what did we agree last month?" from a chat scroll.

The standard AI setup doesn't fix this, because chat assistants are *pull*. You open a tab, you ask, you get an answer, and the context dies when the tab closes. That breaks the moment your work outlives one conversation — when a decision made on Tuesday needs to shape an email on Friday. I didn't want a better chat window. I wanted a chief of staff: something that pushes, remembers, and prepares.

## Two laws, copied from a brain

Everything in the system obeys two principles, and both are stolen from how a brain works.

**First: two layers of memory.** A fast, messy layer you write to without thinking, and a slow, curated layer you trust. Conflating the two is the classic note-taking failure — you end up with either a pristine system you never write to, or a junk drawer you can't rely on. So capture is cheap and deliberately lossy-forward (over-capture, drop later), while curation is slow and gated. Exactly like short-term and long-term memory.

**Second: three verbs.** Every piece of information that enters my world does exactly one of three things — **IN** (get captured), **FILE** (get sorted into permanent memory), or **DO** (become scheduled work). Each verb is owned by a separate process, and the processes never reach into each other's territory. The capture process can't write to the curated brain. The filing process can't touch my calendar. That separation is what keeps the whole thing debuggable as it grows — and it's also why I trust it.

![The system at a glance: two loops around one inbox file](/img/chief-of-staff-at-a-glance.png)

## A junk drawer I can trust

The fast layer is a single append-only file called `inbox.md`. Timestamped one-liners. No schema, no ceremony.

The design choice that matters: capture is *automatic and unprompted*. During any working session, when something notable surfaces — a fact, a decision, a commitment, a stakeholder's exact words — the agent appends a dated line to the inbox without asking me. I can force a capture ("log this") or suppress one ("off the record"), but the default is that nothing gets lost because I was too busy to write it down. A junk line costs nothing to delete later. A lost signal is gone forever.

Then there's the part that changed everything: a timer. Every morning, before I'm at my desk, an unattended agent session wakes up, reads my email and chat, judges what's material against my live workstreams and key people, and writes a digest into the inbox. By the time I sit down, the outside world has already been triaged. The single highest-leverage change in the whole system was this flip from pull to push — from "I have to remember to ask" to "it's waiting for me." A small hook completes the trick: every new session starts pre-loaded with the recent inbox tail and the vault's index, so the agent is never cold.

And why flat files instead of a database? Because when something misbehaves, I debug a file, not a service. Everything in this system can be inspected with `cat` and `grep`.

## The vault: a wiki that maintains itself

The slow layer is where it gets interesting. My permanent memory is a curated vault of Markdown pages that I browse in Obsidian — projects, people, systems, concepts, decisions — densely wikilinked into something that behaves less like a folder of notes and more like a neural network. If I open the page on delivery windows, it's linked to lead times, to chargebacks, to a capacity workflow we're building. Every topic in my world knows which other topics it touches.

Here's the thesis behind it. Every knowledge system ever invented — Zettelkasten, Notion, the wiki you abandoned — is good at *capture*. None of them solve *maintenance*. Keeping cross-links current, flagging contradictions when a new source disagrees with an old one, re-summarising as understanding evolves: that work grows faster than the value of the collection, so humans give up, and the second brain rots into a junk drawer.

The way out is a division of labour: **capture needs human taste; maintenance needs infinite patience.** So I split them. I decide what enters the vault and what it means. The LLM does everything else — summarising, cross-referencing, filing, bookkeeping. It doesn't get bored, so the maintenance cost that kills every human wiki drops toward zero.

This is an old dream. In 1945, Vannevar Bush described the Memex: a personal knowledge store where associative trails between documents matter as much as the documents themselves. The piece he could never solve was who does the labour of maintaining the trails. Eighty years later, there's an answer.

The vault runs on a small set of named operations. *Ingest* reads a source in full, proposes which pages it should touch, and waits for my go-ahead before writing — one dense source can update ten or fifteen pages. *Query* answers questions with citations and is forbidden from modifying anything; reading and writing never mix. *Lint* is the maintenance sweep no human ever does voluntarily: find contradictions between pages, flag stale claims, surface topics mentioned three times that deserve their own page. And two disciplines run through all of it: nothing fabricated, ever — an inferred claim is marked `(inferred)`, never laundered into fact — and contradictions are surfaced, not silently resolved. The vault is allowed to hold tension. Real knowledge does.

The framing I keep coming back to: Obsidian is the IDE, the LLM is the programmer, and the wiki is the codebase. I read; it writes; the knowledge compounds.

## Evenings end with one word

Each evening I type one word: **file**.

The filing agent reads the inbox, the day's meeting notes, the chat logs — and sorts. The unambiguous, primary-source items get filed into the vault automatically. Everything that requires judgment gets surfaced back to me in a tight "needs review / needs action" report. It is conservative by design: when in doubt, it leaves the item where it is and flags it, rather than guessing its way into my permanent memory.

This is the gate between the two layers, and it's where the cognition lives. Low friction going in, high scrutiny going through. Not every email I receive deserves to become a permanent fact about my world — but every email gets *considered*.

One small trick connects knowledge to action: anything carrying an ask, a deadline, or a decision gets a single tag at capture time. The filing process ignores the tag and files the facts. The scheduling process consumes *only* the tagged items. Two systems, one shared file, one discriminating tag — and they never collide.

## Mornings start with "what's cooking"

Which brings us back to Donna. She owns the action loop, and her core rule is what I call the triple-record: every real task exists in three places or it doesn't exist at all — a row in the task log with a stable ID, a to-do in the task app, and a calendar block whose title carries that same ID. If only two of the three exist, the job is half-done.

She's opinionated about priority (importance times urgency, with stakeholder seniority as a signal), she reads the *live* calendar before proposing anything, and she respects red lines I've drawn around my own time — no work blocks before a set hour, lunch is sacred, focus days stay whole. She proposes; she does not book over my life.

Because I filed the night before, she's current. So my first move of the day is asking her what's cooking, and my second is reading the brief — in detail, every line. Then I go straight to the two or three things that need my actual brain: reading deeply, deciding. The stakeholder notes get drafted for me, in my voice, by a writer skill that carries my house style — Donna doesn't write them herself; she frames the job and hands it to a specialist, the way a real chief of staff would. Nothing it drafts exists anywhere except a drafts folder until I've approved the exact words. The file-moving, the log-keeping, the formatting — none of that touches my morning anymore.

## The hits I took

Now the part most write-ups of AI systems skip.

This system has embarrassed me. Early on, I let it draft and send email with too much autonomy, and one went out carrying information that was wrong. Not catastrophically wrong — but wrong, with my name on it, read by people whose time I respect. I sent the correction myself the same day and owned it. The model hadn't failed; my architecture had. I had granted autonomy in exactly the place where mistakes are most expensive: the moment something leaves my machine and lands in front of another human.

So I rebuilt around one constitutional rule: **nothing outbound without my explicit, message-specific approval.** No email, no chat message, no invite goes out without me seeing the exact text. Draft, show, wait. This rule outranks every other instruction in the system.

And for anything that reaches my manager or senior stakeholders, the bar goes higher still: every factual claim must trace to a primary source the agent actually read. No reasoning from vibes. No confident filler. That requirement beats every prompt, every persona, every convenience.

The deeper lesson is about *how* you enforce rules like these. "Please don't send email" is a request — and a sufficiently confused agent will eventually route around a request. So the morning unattended job doesn't rely on politeness: the send tools are simply absent from its toolset, with a denylist behind that, and the prompt prohibition behind that. Three independent layers, any one of which stops an outbound action. A request can be ignored. A missing tool cannot.

If you take one thing from this essay: mechanical guardrails over instructed ones, anywhere the action is irreversible.

Put together — the memory files, the skills, the gates — the full system looks like this:

![The full wiring: memory, skills, and the outbound gate](/img/chief-of-staff-full-wiring.png)

## Slower on purpose

The other honest admission: this was not free. There were weeks where doing a task through the system took longer than doing it by hand — noticeably longer — and I did it through the system anyway. Forceful teaching. Every correction became a permanent memory file the agent loads at the start of every session: never send without approval, always show task IDs with their titles, this stakeholder needs proposal-first framing. Dozens of small, hard-won rules.

That's the trade most people refuse: pay a tax now so the assistant stops re-learning you. A year in, the assistant knows how I work the way a long-tenured chief of staff would — and the tax was paid once.

## What it feels like now

My day collapses into two moves. In the evening: *file*. In the morning: *what's cooking*. Capture runs itself on a timer. The vault answers "what do I know?" with citations. Donna answers "what do I do?" with a calendar that respects my boundaries. And nothing leaves for another human without my eyes on the exact words.

If you build your own version, the decisions that earned their keep: flip from pull to push with one unattended morning run; let the machine write freely where mistakes are cheap and gate it hard where they're expensive; keep state in deterministic code, never in the model; and prefer guarantees to requests for anything you can't take back.

The architecture transfers, too. Outside the day job, I run a lighter rebuild of this for a personal project — same patterns, a different Donna, and a second agent named Jessica who owns the roadmap. The system doesn't care whether the inbox belongs to a product manager or a founder. That, more than anything, is what convinced me this is a pattern and not a party trick.

I started this because I wanted my hours back for the only thing a PM is actually paid for: judgment. A year later, the surprise isn't the time saved. It's that the quality of my decisions went up — because every decision now starts from a brief, grounded in everything I know, prepared by a colleague who never forgets.

She just doesn't exist.

*If you're working out where AI actually fits in your business — not the demos, the daily workflows — I enjoy comparing notes. My inbox is open. Donna triages it.*
