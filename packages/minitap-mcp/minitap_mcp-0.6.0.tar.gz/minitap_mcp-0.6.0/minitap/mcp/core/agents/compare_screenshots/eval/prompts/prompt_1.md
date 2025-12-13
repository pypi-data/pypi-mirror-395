You will be given _two screenshots_.

1. "Expected screenshot" — this is the design from Figma.
2. "Implemented screenshot" — this is the actual phone screen that has been built.

Your task is to **compare the two screenshots** in detail, and generate a structured report that includes:

- A comprehensive list of **all visible differences** between the expected design and the implemented screen.
- For each difference, provide:
  - A clear **description** of what changed (for example: "The 'Submit' button label changed from 'Submit' to 'Send'", "The icon moved 8px to the right", "The background colour of header changed from #FFFFFF to #F6F6F6", etc.).
  - The **type of change** (e.g., text change, color change, position/movement, size change, added element, removed element, style change).
  - The **location** of the change (for example: "bottom-centre of screen", "top header area", "to the right of search bar"). If possible, approximate coordinates or bounding box (e.g., "approx. 240×180 px at screen width 1080").
  - The **impact on implementation** (i.e., reasoning about what this means: "The implemented version uses a different text label – so behaviour may differ", "The icon moved and may overlap another element", etc.).
  - A **recommendation** if relevant (e.g., "Should revert to #FFFFFF to match design", "Check alignment of icon relative to search bar", etc.).

**Important**:

- Assume the screenshots are aligned (same resolution and scale); if not aligned mention that as a difference.
- Focus on _visible UI differences_ (layout, text, style, iconography) – you do _not_ need to inspect source code, only what is visually rendered.
- Do _not_ produce generic comments like "looks like a difference" – aim for _precise, actionable descriptions_.
- **IGNORE dynamic/personal content** that naturally differs between mockups and real implementations:
  - User profile information (names, usernames, email addresses, profile pictures)
  - Time-based information (current time, dates, timestamps, "2 hours ago", etc.)
  - Dynamic data (notification counts, unread badges, live statistics)
  - Sample/placeholder content that varies (e.g., "John Doe" vs "Jane Smith")
  - System status information (battery level, signal strength, network indicators)
  - Only flag these as differences if the _structure, layout, or styling_ of these elements differs, not the content itself.
- Output in a structured format, for example:

```

1. Location: [top header – full width]
   Change: Background colour changed from #FFFFFF → #F6F6F6
   Type: Colour change
   Impact: The header will appear darker than design; text contrast may be lower.
   Recommendation: Update header background to #FFFFFF as in design.

```

- At the end produce a summary with ONLY:
  - Total number of differences found
  - Overall "match score" out of 100 (your estimation of how closely the implementation matches the design)
  - Do NOT include any recap, overview, or macro-level summary of changes - all details are already captured in the differences list above.

### Input:

- Screenshot A: Expected (Figma)
- Screenshot B: Implemented (Phone)
  Provide both screenshots and then the prompt.

### Output:

Structured list of differences + summary.

Please use the following to start the analysis.
**Input:**
First screen is the Figma screenshot (what is expected)
Second screen is what is implemented (taken from the phone, after the implementation)

You will have this data in the next messages sent by the user.

Go ahead and generate your report.
