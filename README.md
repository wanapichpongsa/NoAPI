# NoAPI

NoAPI is a custom NLP library for you to parse document files into app-friendly data formats.

## Example Usage

**The following example was the fintech-related problem I faced. This project is not finance specific and can be used for general ETL tasks.**

You want to make an annual pie chart and line chart of spending by categories.

Easiest solution: Make an Excel spreadsheet, then use their chart maker!

Problem: This is what your bank statement PDF looks like 👇

```
ACCOUNT SUMMARY

DATE | TO WHOM | DETAILS | OUTFLOW | INFLOW | BALANCE

e.g.,
01/01/2025 | SUPERMARKET_NAME | CITY | 100.00 | 0.00 | 900.00
           | OPENAI | CITY | 200.00 | 0.00 | 700.00
           | JEFF | For Dinner | 0.00 | 25.00 | 725.00

... PARAGRAPHS OF TEXT ...
```
You can obviously manually translate the document into an excel file, but imagine deciding which invoice belongs to which category for hundreds to thousands of transactions.

The better solution is to designate categories for your dataframe

Example dataframe structure:
```python3

### DISCLAIMER: This is just arbitrary pseudocode. I don't know what the ideal structure layout is yet.
spending_categories: dict[str, any] {
  health: {
    exercise: {
      gym: 100.00,
      gym_travel: 20.00 # very hard
    },
    food: {
      groceries: {
        chicken_breast: 4.00
        rice_white: 4.00
      },

      restaraunts {
        ...
      },

      delivery {
        ...
      }

    }
  },
  investing: {
    # FYI: Trading platform names
    robin_hood: 5000.00,
    binance: 5000.00
  }
}
### Things we can add for spending_categories dictionary
# 1. Make another nested dict for useful columns: 1. entity

# Investments are a whole different beast (e.g., changing real-time, need growth projections features)
# Beware of naming conflicts
investments: {
  robin_hood: {
    index_funds: {
      VOO: {
        tech: {
          AAPL: MarketPrice * IndexFundAllocation (%)
        }
      }
    },

    stock_picking: {
      tech: {
        NVDA: {
          "Potential_PL": Price_Bought * Quantity - Price_Now * Quantity
          "PL": if sold: Potential_PL else None
        }
      }
    }
  }
}
```

and have your LLM of choice allocate each invoice to each category! Ideally, it would be great if:
1. The LLM learns how to think of categories that the user missed and appends it to the dataframe
2. The LLM learns to suggest removal of redundant categories.
(That's a bug-fest awaiting so ceebs rn)

(For privacy reasons, I prefer Ollama because I want my data to be processed locally)

Imagine the Excel Output:
- Sheet 1: Each individual row allocated to their respective category
- Sheet 2: Statistical calculations you want to perform e.g., sum, mean, stdev, projections

Sheet 1 will tell you whether your data is messed up.
Sheet 2 is what you use to perform data visualisation for your user 🎉

Additional thoughts:

For easy cross-checking, associate original invoice id(s) as metadata.

LLM Error Handling:
1. Gives confidence score from 0 - 1.0
2. If score < 0.7 allocate 'unsure'

That's it for my rant. Enjoy, and please give me feedback!

**Disclaimer:** Project beta version is under development. Open to changing name if it is a bad fit.

## Features
List TBD

## Dependencies

- streamlit: Python scripts into shareable app in seconds
- pandas: Data analysis equation functions and structure
- ollama: Deepseek R1 local model
- plotly: HTML exportable data visualisation


## Installation

Right now working on bank statement parser. If you want to help me:

1. Clone the repository:
```bash
git clone https://github.com/{yourusername}/NoAPI
cd NoAPI
```


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

This means that any modified versions of this software must also be made available under the GPL v3.0 license. This ensures that improvements to the code remain free and open source.

## Acknowledgments

- @arsenstorm for debugging assistance and regex pattern optimization