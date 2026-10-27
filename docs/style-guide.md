# Style guide

The standard these samples follow. Based on the Google developer documentation style guide, with the decisions this portfolio needed.

## Voice and person

- Second person for instructions: "You create a room."
- First person only for the author's own actions or opinions.
- Active voice. If the actor matters and is unknown, the passive is acceptable once, not twice in a paragraph.
- Present tense for what the software does. "The service returns a 400" not "the service will return a 400".
- No contractions in reference pages. Contractions are fine in guides and tutorials.

## Structure

- **One heading level 1 per page**, equal to the page title.
- Heading text is a noun phrase for reference pages, a verb phrase for how-tos. "Create a room", not "Creating a room" and not "Room creation".
- Steps are numbered lists, one action per step, imperative. Notes about a step go inside the step, indented, not after the list.
- Three or more parallel items become a table; prose lists are for two items.
- A page over roughly 800 words gets a "On this page" navigation or is split.

## Terminology

Decision list. Left is correct, right is banned, and why.

| Use | Do not use | Reason |
| --- | --- | --- |
| sign in | log in, login | Same verb for noun and verb, matches the UI |
| set up (verb), setup (noun) | setup as a verb | Two forms, two jobs |
| endpoint | API call, API route, URL | One word for one concept |
| request, response | call, reply | Precise about the HTTP exchange |
| repository | repo (in reference pages) | Full word in reference, short form in chat |
| delete | remove, drop | One verb, one consequence |
| gaze deviation | eye tracking accuracy | The metric is deviation in degrees, not accuracy |
| session | interview (in API reference) | The API object is a session; the product concept is an interview |

Product names keep their casing exactly: InViewAI, Mafia, FastAPI, Socket.IO, Firestore, Cloudinary.

## Formatting

- Code, paths, commands, environment variables and field names in backticks. Nothing else.
- Placeholders in angle brackets and uppercase in prose (`<SESSION_ID>`), in `$UPPER_SNAKE` form inside shell examples.
- Every shell example is one copyable block. No mixing of comments and commands that a reader would paste blindly.
- JSON examples are complete and valid. Truncated JSON gets a comment saying what was cut.
- Emphasis is for warnings only. If everything is bold, nothing is.
- No exclamation marks, no "simply", "easily", "just", "obviously". If it were simple, the page would not exist.

## Warnings and notes

Three callout types, in order of severity:

- **Warning**: data loss, cost, security, or an irreversible action.
- **Note**: a behavior that surprises people but is safe.
- **Tip**: an optional shortcut that saves time.

Every warning names the consequence. "This deletes the session state" is a warning. "Be careful" is noise.

## Accessibility

- Alt text on every image, describing the information not the pixels: "Response panel showing `face_detected: false`" not "screenshot".
- No meaning carried by color alone.
- Table headers on every table, never a table used for layout.
- Link text says where it goes: "the authentication section" not "click here".
