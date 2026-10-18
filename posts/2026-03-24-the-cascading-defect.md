title: The Cascading Defect
dek: Why one bad barcode costs you more than you think — and why fixing it is an agent problem, not a dashboard problem.
date: 2026-03-24
slug: the-cascading-defect
---

There's a type of problem in e-commerce operations that I find genuinely fascinating. Not because it's glamorous — it's the opposite. It's so boring that most businesses refuse to look at it. And that refusal is exactly what makes it so expensive.

I'm talking about catalogue defects. The unglamorous backbone of every product you sell online: your barcodes, your case pack configurations, your external IDs, your packaging hierarchies. The data that tells a warehouse system what it's looking at when it scans a box.

When this data is wrong, the consequences don't show up as a single error. They cascade.

## The anatomy of a cascade

Here's a real scenario. A brand sells shampoo in two sizes: 250ml and 500ml. Different products, different prices, different barcodes. Except — someone during onboarding linked the same EAN barcode to both ASINs in the marketplace's internal catalogue.

On day one, nothing happens. The products sit in a warehouse. Orders come in. Life goes on.

Then a purchase order arrives for 500 units of the 250ml bottle. The warehouse ships them. The marketplace's receiving system scans the barcode and — because the catalogue maps that barcode to *both* products — receives half against the 500ml product instead. The vendor's invoice says 500 units of 250ml. The marketplace's records say they received 250 of the 250ml and 250 of the 500ml.

Result: a shortage claim on the 250ml (the marketplace says it only received 250, not 500). And an unexplained overage on the 500ml (suddenly 250 units appeared that nobody ordered).

The vendor disputes the shortage. The dispute takes 45–79 days. Maybe they win, maybe they don't. Meanwhile, the same barcode error fires again on the next shipment. And the next.

Now multiply this across a catalogue of 500 products with variant sizes, colours, and regional packaging differences. The brand is haemorrhaging money through a wound it can't even see — because no individual chargeback is big enough to investigate, but collectively they represent 2–4% of annual revenue quietly evaporating.

## Five types, one root cause

What I find interesting is how many different penalties trace back to catalogue data. It's not just barcode conflicts. There are at least five distinct failure modes, and they all share the same DNA:

**Case pack mismatches.** The catalogue says a case contains 6 units. The vendor actually ships cases of 12. The receiving system scans the case barcode and records 6. Vendor invoices 12. Shortage: 6 units per case, every shipment.

**Barcode-to-product conflicts.** One barcode linked to multiple products. The scan goes to the wrong product, creating phantom shortages and phantom overages simultaneously.

**External ID drift.** The barcode on the purchase order doesn't match the barcode on the invoice, because someone updated the product's barcode in the catalogue but the PO was generated before the update took effect. The matching system can't reconcile the two.

**Missing packaging hierarchy data.** The marketplace doesn't know how many cases fit on a pallet, or what the case dimensions are. In some regions this has caused a 15–20% increase in receiving errors — not from vendor mistakes, but from the system guessing wrong about what a pallet should look like.

**Invoice-to-receipt mismatches.** The PO references a case-level barcode. The invoice references a unit-level barcode. Same product, different identifiers. The matching system sees two unrelated items.

Every single one of these is a data problem, not an operational failure. The vendor shipped the right product. The warehouse received correctly. But the system's model of reality didn't match physical reality — and the vendor pays the penalty.

## Why this is an agent problem, not a dashboard problem

Here's where it gets interesting for anyone thinking about AI.

The standard approach to this is: build a dashboard, let someone review chargebacks weekly, dispute the big ones. This is fine for recovering money you've already lost. It does nothing about the structural defect generating the losses.

The structural fix requires something different. You need to crawl an entire product catalogue — hundreds or thousands of SKUs — and cross-reference each one against case pack data, barcode registries, purchase order history, invoicing records, and receiving reports. You need to spot mismatches that span multiple systems and multiple time periods. You need to distinguish between a one-off anomaly and a systemic defect that fires every shipment.

This is exactly the kind of work that's too tedious for a human analyst to do comprehensively, and too unstructured for a simple rules engine to catch.

It's an agent problem.

Not one agent — a team of agents. One agent that understands catalogue structure and can audit barcode-to-product relationships. One that reads purchase order history and flags recurring shortage patterns on the same product codes. One that cross-checks invoice external IDs against PO external IDs looking for drift. One that compiles findings from the other agents and ranks defects by financial impact: "Fix these 8 catalogue entries. Estimated annual savings: £47,000."

The individual checks are straightforward. The value is in the orchestration — running all of them in parallel across an entire catalogue, then synthesising the findings into a prioritised action list.

This is what multi-agent systems are actually good at. Not generating marketing copy or summarising documents — those are party tricks. The real value is in coordination across messy, cross-system data where no single query gives you the answer but a team of focused investigations does.

## The cascade works in reverse too

The beautiful thing about fixing catalogue defects is that the benefits cascade just like the costs did.

Fix a barcode conflict and the shortage claims stop. The overage penalties stop. The dispute effort disappears. The receiving accuracy improves. The inventory records become trustworthy, which means your demand forecasting gets cleaner data, which means your purchase orders are more accurate, which means your stockout rate drops, which means your sales go up.

One entry in a catalogue database. Six downstream improvements.

I keep coming back to this principle: the most impactful problems in e-commerce operations are the ones nobody wants to look at. They're buried in data quality, in catalogue hygiene, in the boring plumbing that connects systems together. They're not strategic. They're not interesting to talk about at conferences.

But a brand doing £5M through marketplaces with a 3% leakage rate from catalogue-driven penalties? That's £150K a year. Quietly, invisibly, permanently — until someone finally audits the data.

## What's coming

I think the next wave of useful AI in commerce operations won't be the consumer-facing chatbot or the AI-generated product description. It'll be agent teams working behind the scenes on exactly this kind of problem: silent, cross-system audits that surface structural defects before they compound.

The technology is ready. The data is available (most marketplace APIs expose catalogue, PO, and chargeback data). The economic incentive is clear.

What's missing is someone framing this as a product problem worth solving, rather than a consulting exercise you run once and hope for the best.

I think that's about to change.
