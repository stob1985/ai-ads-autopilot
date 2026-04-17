# inputs/

Drop two files here before running the pipeline.

## `creator.jpg`

Your face — this becomes the HeyGen photo avatar.

- Front-facing, eye-level
- Good even lighting, no harsh shadows
- No sunglasses, hats pulled back, hair off the face
- Plain-ish background beats a busy one
- 1024px+ on the short edge

## `product.png`

Your product — this is passed as a reference image to Gemini on **every** ad generation so the packaging stays pixel-accurate.

- Transparent or plain white background (PNG strongly preferred)
- 2000px+ on the long edge
- The label should be readable — if text is blurry on the source, it will be blurry in the ads
- One product per file — if you have a bundle, grab the hero SKU

### Level 3 (autopilot) — multiple products

Put each product in its own file inside `inputs/products/` and point `products.yaml` at them:

```
inputs/
├── creator.jpg
└── products/
    ├── matcha.png
    ├── drops.png
    └── bars.png
```

Both `inputs/creator.jpg` and anything inside `inputs/products/` are gitignored.
