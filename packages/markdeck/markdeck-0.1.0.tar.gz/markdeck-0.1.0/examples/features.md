# MarkDeck Features

Comprehensive feature showcase

---

## Speaker Notes

This slide demonstrates speaker notes functionality.

Press 'S' to toggle speaker notes view.

<!--NOTES:
These are speaker notes. They are hidden from the main presentation view but visible when you press 'S'.

Use speaker notes to:
- Remember key points
- Add talking points
- Keep timing notes
- Store additional context
-->

---

## Advanced Code Highlighting

Python with type hints:

```python
from typing import List, Optional

def process_data(items: List[str], limit: Optional[int] = None) -> dict:
    """Process a list of items and return statistics."""
    result = {
        'count': len(items),
        'items': items[:limit] if limit else items
    }
    return result
```

---

## More Language Support

Rust:

```rust
fn main() {
    let numbers = vec![1, 2, 3, 4, 5];
    let sum: i32 = numbers.iter().sum();
    println!("Sum: {}", sum);
}
```

SQL:

```sql
SELECT users.name, COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id
HAVING order_count > 5;
```

---

## Complex Tables

| Feature | MarkDeck | PowerPoint | Google Slides |
|---------|-----------|------------|---------------|
| Markdown | ✓ | ✗ | ✗ |
| Version Control | ✓ | ✗ | ✗ |
| Lightweight | ✓ | ✗ | ✗ |
| Syntax Highlighting | ✓ | Limited | Limited |
| Free | ✓ | ✗ | ✓ |
| Open Source | ✓ | ✗ | ✗ |

---

## Text Formatting

You can use **bold**, *italic*, ***bold italic***, ~~strikethrough~~, and `inline code`.

You can also combine them: **bold with `code`** and *italic with `code`*.

---

## Block Quotes

> "Simplicity is the ultimate sophistication."
>
> — Leonardo da Vinci

> Multi-paragraph quotes work too.
>
> Just add blank lines between paragraphs within the quote block.

---

## Horizontal Rules

Content above

---

**Note**: The slide delimiter `---` must be on its own line with newlines before and after.

---

## Lists with Nesting

Complex nested structure:

1. First level
   - Nested bullet
   - Another bullet
     - Even deeper
     - More depth
2. Back to first level
   1. Nested number
   2. Another number
3. Final item

---

## Definition Lists (via Markdown)

**Term 1**
: Definition of term 1

**Term 2**
: Definition of term 2
: Alternative definition

**Term 3**
: Another definition

---

## Math (Future Feature)

In future versions, we plan to support math equations:

- Inline math: E = mc²
- Display math equations
- Chemical formulas
- Complex expressions

---

## Mermaid Diagrams (Future)

Future support for diagrams:

- Flowcharts
- Sequence diagrams
- Gantt charts
- Class diagrams

---

## Two-Column Layout (Planned)

This is a planned feature for future releases.

You'll be able to split slides into columns:

- Left column content
- Right column content

---

## Performance

MarkDeck is designed to be:

- **Fast**: Minimal JavaScript, no heavy frameworks
- **Lightweight**: Small bundle size
- **Efficient**: Smooth navigation even with 100+ slides
- **Responsive**: Works on different screen sizes

---

## Customization Options

Future customization features:

- Custom themes
- Color schemes
- Font choices
- Transition effects
- Layout templates

---

## Export Options (Planned)

Planned export formats:

- PDF (via print)
- Standalone HTML
- PowerPoint (maybe)
- PNG images

---

## Use Cases

Perfect for:

- Technical presentations
- Code reviews
- Conference talks
- Teaching materials
- Documentation
- Lightning talks

---

## Open Source

MarkDeck is open source (MIT License).

Contributions welcome:
- Bug reports
- Feature requests
- Pull requests
- Documentation improvements

---

## Thank You!

Try MarkDeck for your next presentation.

Press 'S' to see speaker notes throughout this deck.
