# Content And Trust

Content is part of the interface. Good UX writing reduces hesitation because users can predict what will happen.

## Labels And Actions

Prefer labels that include object and action:

- Weak: `Submit`
- Better: `Save invoice`
- Better: `Invite teammate`
- Better: `Publish draft`
- Better: `Retry sync`

Avoid generic labels when the action has consequence:

- `Get started`
- `Learn more`
- `Continue`
- `Next`
- `Confirm`
- `AI powered`
- `Magic`
- `Optimize`

These are acceptable only when surrounding context makes the destination or object unambiguous.

## Help Text

Help text should:

- sit near the decision
- explain constraints, examples, consequence, or privacy
- be shorter than the confusion it prevents
- disappear when the design can make the same thing obvious

Do not use help text as a bandage for a bad flow.

## Errors

Error messages should say:

1. What happened.
2. What field/object/action is affected.
3. What the user can do.
4. Whether their data was saved.

Pattern:

```text
We could not save the payment method. Check the card number or try another card. Your order details are still saved.
```

Avoid:

- `Something went wrong`
- `Invalid input`
- `Error`
- `Oops`
- blaming tone
- unexplained error codes

## Empty States

Good empty states answer:

- Why is this empty?
- Is this expected?
- What can the user do next?
- What will appear here later?

Do not fill empty states with fake data unless it is clearly sample data and cannot be mistaken for real user activity.

## Trust-Sensitive Claims

Require evidence or scope for:

- live metrics
- uptime
- security
- compliance
- payments
- integrations
- AI output
- automation
- testimonials
- user counts
- revenue
- health, finance, legal, or safety advice

If evidence is unavailable:

- remove the claim
- label it sample/demo/local
- disable the capability with reason
- describe the required configuration

## AI UX

AI interfaces must set expectations:

- what input the model needs
- what it can and cannot do
- whether sources are available
- whether output is draft, suggestion, or committed fact
- how to edit, regenerate, cite, reject, or report
- what happens if generation fails
- where human review is required

Do not use AI as a black-box confidence theater. Show useful boundaries without drowning the user in model internals.

## Confirmation And Consent

Ask for confirmation when:

- action is destructive
- action sends data outside the current workspace
- action cannot be undone
- action affects billing, permissions, publication, security, privacy, or other people

Do not ask for confirmation for harmless repeated actions. Use undo instead when safer and faster.

