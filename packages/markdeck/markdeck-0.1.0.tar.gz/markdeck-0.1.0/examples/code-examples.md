# Code Examples Showcase

Demonstrating syntax highlighting across multiple languages

---

## Python

```python
# Data processing example
import pandas as pd
from typing import List, Dict

class DataProcessor:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def analyze(self) -> Dict[str, float]:
        """Analyze the dataset and return statistics."""
        return {
            'mean': self.data.mean().mean(),
            'std': self.data.std().mean(),
            'count': len(self.data)
        }
```

---

## JavaScript / TypeScript

```typescript
// React component example
interface User {
    id: number;
    name: string;
    email: string;
}

const UserProfile: React.FC<{ user: User }> = ({ user }) => {
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchUserData(user.id);
    }, [user.id]);

    return <div className="profile">{user.name}</div>;
};
```

---

## Rust

```rust
// Ownership and borrowing example
use std::collections::HashMap;

fn count_words(text: &str) -> HashMap<String, usize> {
    let mut counts = HashMap::new();

    for word in text.split_whitespace() {
        *counts.entry(word.to_lowercase()).or_insert(0) += 1;
    }

    counts
}

fn main() {
    let text = "hello world hello rust";
    let word_counts = count_words(text);
    println!("{:?}", word_counts);
}
```

---

## Go

```go
// Concurrency example
package main

import (
    "fmt"
    "sync"
)

func worker(id int, jobs <-chan int, results chan<- int, wg *sync.WaitGroup) {
    defer wg.Done()
    for job := range jobs {
        fmt.Printf("Worker %d processing job %d\n", id, job)
        results <- job * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)
    var wg sync.WaitGroup

    // Start workers
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go worker(i, jobs, results, &wg)
    }

    // Send jobs
    for j := 1; j <= 9; j++ {
        jobs <- j
    }
    close(jobs)

    wg.Wait()
    close(results)
}
```

---

## Java

```java
// Stream API example
import java.util.*;
import java.util.stream.*;

public class StreamExample {
    public static void main(String[] args) {
        List<Person> people = Arrays.asList(
            new Person("Alice", 30),
            new Person("Bob", 25),
            new Person("Charlie", 35)
        );

        Map<Integer, List<Person>> byAge = people.stream()
            .filter(p -> p.getAge() > 25)
            .collect(Collectors.groupingBy(Person::getAge));

        System.out.println(byAge);
    }
}
```

---

## C++

```cpp
// Modern C++ example
#include <iostream>
#include <vector>
#include <algorithm>
#include <memory>

template<typename T>
class SmartContainer {
private:
    std::vector<std::unique_ptr<T>> items;

public:
    void add(T* item) {
        items.push_back(std::unique_ptr<T>(item));
    }

    void process() {
        std::for_each(items.begin(), items.end(),
            [](const auto& item) {
                item->execute();
            });
    }
};
```

---

## SQL

```sql
-- Complex query example
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date) AS month,
        product_id,
        SUM(quantity * price) AS revenue
    FROM orders
    JOIN order_items USING (order_id)
    WHERE order_date >= '2024-01-01'
    GROUP BY 1, 2
),
ranked_products AS (
    SELECT
        month,
        product_id,
        revenue,
        ROW_NUMBER() OVER (PARTITION BY month ORDER BY revenue DESC) AS rank
    FROM monthly_sales
)
SELECT * FROM ranked_products
WHERE rank <= 10
ORDER BY month, rank;
```

---

## Shell Script

```bash
#!/bin/bash
# Deployment script

set -euo pipefail

ENVIRONMENT=${1:-production}
APP_NAME="myapp"

echo "Deploying $APP_NAME to $ENVIRONMENT..."

# Build application
docker build -t "$APP_NAME:latest" .

# Run tests
docker run --rm "$APP_NAME:latest" pytest

# Deploy
if [ "$ENVIRONMENT" = "production" ]; then
    kubectl apply -f k8s/production/
    kubectl rollout status deployment/"$APP_NAME"
else
    kubectl apply -f k8s/staging/
fi

echo "Deployment complete!"
```

---

## JSON

```json
{
  "name": "markdeck",
  "version": "0.1.0",
  "description": "A lightweight markdown presentation tool",
  "dependencies": {
    "fastapi": "^0.104.0",
    "uvicorn": "^0.24.0",
    "python-markdown": "^3.5.0"
  },
  "scripts": {
    "dev": "uvicorn markdeck.server:app --reload",
    "test": "pytest",
    "lint": "ruff check ."
  }
}
```

---

## YAML

```yaml
# Docker Compose example
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./app:/app
    command: uvicorn main:app --host 0.0.0.0 --reload

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

---

## HTML/CSS

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Example</title>
    <style>
        .container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>Hello, World!</h1>
        </div>
    </div>
</body>
</html>
```

---

## Inline Code

You can also use inline code: `const result = calculate(42);`

Or with language hints: `python›def hello(): pass` (if supported by your markdown parser)

---

## Code Without Highlighting

Sometimes you want plain text:

```
Plain text code block
No syntax highlighting
Just monospace font
```

---

## Long Code Blocks

```python
# When code is long, the slide container will scroll

class ComplexDataProcessor:
    """A complex data processor with many methods."""

    def __init__(self, config):
        self.config = config
        self.data = []
        self.results = {}

    def load_data(self, source):
        """Load data from source."""
        pass

    def clean_data(self):
        """Clean and preprocess data."""
        pass

    def transform_data(self):
        """Apply transformations."""
        pass

    def analyze_data(self):
        """Run analysis."""
        pass

    def generate_report(self):
        """Generate final report."""
        pass
```

---

## Thank You!

These code examples showcase MarkDeck's syntax highlighting capabilities.

All powered by highlight.js!
