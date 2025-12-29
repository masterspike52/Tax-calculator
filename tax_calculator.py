import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TaxBracket:
    min_income: float
    max_income: float
    rate: float

FEDERAL_BRACKETS_2024 = {
    "Single": [
        TaxBracket(0, 11600, 0.10), TaxBracket(11600, 47150, 0.12),
        TaxBracket(47150, 100525, 0.22), TaxBracket(100525, 191950, 0.24),
        TaxBracket(191950, 243725, 0.32), TaxBracket(243725, 609350, 0.35),
        TaxBracket(609350, float('inf'), 0.37),
    ],
    "Married Filing Jointly": [
        TaxBracket(0, 23200, 0.10), TaxBracket(23200, 94300, 0.12),
        TaxBracket(94300, 201050, 0.22), TaxBracket(201050, 383900, 0.24),
        TaxBracket(383900, 487450, 0.32), TaxBracket(487450, 731200, 0.35),
        TaxBracket(731200, float('inf'), 0.37),
    ],
    "Married Filing Separately": [
        TaxBracket(0, 11600, 0.10), TaxBracket(11600, 47150, 0.12),
        TaxBracket(47150, 100525, 0.22), TaxBracket(100525, 191950, 0.24),
        TaxBracket(191950, 243725, 0.32), TaxBracket(243725, 365600, 0.35),
        TaxBracket(365600, float('inf'), 0.37),
    ],
    "Head of Household": [
        TaxBracket(0, 16550, 0.10), TaxBracket(16550, 63100, 0.12),
        TaxBracket(63100, 100500, 0.22), TaxBracket(100500, 191950, 0.24),
        TaxBracket(191950, 243700, 0.32), TaxBracket(243700, 609350, 0.35),
        TaxBracket(609350, float('inf'), 0.37),
    ],
}

FEDERAL_BRACKETS_2025 = {
    "Single": [
        TaxBracket(0, 11925, 0.10), TaxBracket(11925, 48475, 0.12),
        TaxBracket(48475, 103350, 0.22), TaxBracket(103350, 197300, 0.24),
        TaxBracket(197300, 250525, 0.32), TaxBracket(250525, 626350, 0.35),
        TaxBracket(626350, float('inf'), 0.37),
    ],
    "Married Filing Jointly": [
        TaxBracket(0, 23850, 0.10), TaxBracket(23850, 96950, 0.12),
        TaxBracket(96950, 206700, 0.22), TaxBracket(206700, 394600, 0.24),
        TaxBracket(394600, 501050, 0.32), TaxBracket(501050, 751600, 0.35),
        TaxBracket(751600, float('inf'), 0.37),
    ],
    "Married Filing Separately": [
        TaxBracket(0, 11925, 0.10), TaxBracket(11925, 48475, 0.12),
        TaxBracket(48475, 103350, 0.22), TaxBracket(103350, 197300, 0.24),
        TaxBracket(197300, 250525, 0.32), TaxBracket(250525, 375800, 0.35),
        TaxBracket(375800, float('inf'), 0.37),
    ],
    "Head of Household": [
        TaxBracket(0, 17000, 0.10), TaxBracket(17000, 64850, 0.12),
        TaxBracket(64850, 103350, 0.22), TaxBracket(103350, 197300, 0.24),
        TaxBracket(197300, 250500, 0.32), TaxBracket(250500, 626350, 0.35),
        TaxBracket(626350, float('inf'), 0.37),
    ],
}

STANDARD_DEDUCTIONS = {
    2024: {"Single": 14600, "Married Filing Jointly": 29200, "Married Filing Separately": 14600, "Head of Household": 21900},
    2025: {"Single": 15000, "Married Filing Jointly": 30000, "Married Filing Separately": 15000, "Head of Household": 22500}
}

FICA_RATES = {
    2024: {"ss_rate": 0.062, "ss_cap": 168600, "medicare_rate": 0.0145},
    2025: {"ss_rate": 0.062, "ss_cap": 176100, "medicare_rate": 0.0145}
}

STATE_TAX_DATA = {
    "Alabama": 0.05, "Alaska": 0, "Arizona": 0.025, "Arkansas": 0.044,
    "California": 0.093, "Colorado": 0.044, "Connecticut": 0.0699,
    "Delaware": 0.066, "Florida": 0, "Georgia": 0.0549, "Hawaii": 0.11,
    "Idaho": 0.058, "Illinois": 0.0495, "Indiana": 0.0305, "Iowa": 0.0385,
    "Kansas": 0.057, "Kentucky": 0.04, "Louisiana": 0.0425, "Maine": 0.0715,
    "Maryland": 0.0575, "Massachusetts": 0.05, "Michigan": 0.0425,
    "Minnesota": 0.0985, "Mississippi": 0.047, "Missouri": 0.0495,
    "Montana": 0.0575, "Nebraska": 0.0584, "Nevada": 0, "New Hampshire": 0,
    "New Jersey": 0.0637, "New Mexico": 0.059, "New York": 0.0685,
    "North Carolina": 0.0525, "North Dakota": 0.0295, "Ohio": 0.035,
    "Oklahoma": 0.0475, "Oregon": 0.099, "Pennsylvania": 0.0307,
    "Rhode Island": 0.0599, "South Carolina": 0.064, "South Dakota": 0,
    "Tennessee": 0, "Texas": 0, "Utah": 0.0465, "Vermont": 0.0875,
    "Virginia": 0.0575, "Washington": 0, "West Virginia": 0.0512,
    "Wisconsin": 0.0765, "Wyoming": 0, "District of Columbia": 0.1075,
}

# IRS Filing Requirements for 2024 (filing in 2025)
# Based on: https://www.irs.gov/filing/do-i-need-to-file-a-tax-return
FILING_REQUIREMENTS_2024 = {
    "Single": {"under_65": 14600, "65_or_older": 16550},
    "Married Filing Jointly": {
        "both_under_65": 29200,
        "one_65_or_older": 30750,
        "both_65_or_older": 32300
    },
    "Married Filing Separately": {"any_age": 5},
    "Head of Household": {"under_65": 21900, "65_or_older": 23850},
}

# IRS Filing Requirements for 2025 (filing in 2026) - estimated based on inflation adjustments
FILING_REQUIREMENTS_2025 = {
    "Single": {"under_65": 15000, "65_or_older": 17000},
    "Married Filing Jointly": {
        "both_under_65": 30000,
        "one_65_or_older": 31550,
        "both_65_or_older": 33100
    },
    "Married Filing Separately": {"any_age": 5},
    "Head of Household": {"under_65": 22500, "65_or_older": 24500},
}

FILING_REQUIREMENTS = {2024: FILING_REQUIREMENTS_2024, 2025: FILING_REQUIREMENTS_2025}


class TaxCalculator:
    def __init__(self, tax_year: int = 2024):
        self.tax_year = tax_year
        self.federal_brackets = FEDERAL_BRACKETS_2024 if tax_year == 2024 else FEDERAL_BRACKETS_2025
        self.fica = FICA_RATES[tax_year]
        self.standard_deductions = STANDARD_DEDUCTIONS[tax_year]
        self.filing_requirements = FILING_REQUIREMENTS[tax_year]

    def calculate_federal_tax(self, taxable_income: float, filing_status: str) -> Tuple[float, List[dict]]:
        brackets = self.federal_brackets[filing_status]
        total_tax = 0
        breakdown = []
        remaining = taxable_income

        for bracket in brackets:
            if remaining <= 0:
                break
            bracket_size = bracket.max_income - bracket.min_income
            taxable_in_bracket = min(remaining, bracket_size)
            bracket_tax = taxable_in_bracket * bracket.rate
            total_tax += bracket_tax

            if taxable_in_bracket > 0:
                breakdown.append({
                    "bracket": f"${bracket.min_income:,.0f}-${bracket.max_income:,.0f}" if bracket.max_income != float('inf') else f"${bracket.min_income:,.0f}+",
                    "rate": f"{bracket.rate * 100:.1f}%",
                    "income": taxable_in_bracket,
                    "tax": bracket_tax
                })
            remaining -= taxable_in_bracket

        return total_tax, breakdown

    def check_filing_requirement(self, gross_income: float, filing_status: str, 
                                  age_65_or_older: bool, spouse_65_or_older: bool = False) -> dict:
        """Check if taxpayer is required to file based on IRS requirements."""
        requirements = self.filing_requirements[filing_status]
        
        if filing_status == "Single" or filing_status == "Head of Household":
            threshold = requirements["65_or_older"] if age_65_or_older else requirements["under_65"]
        elif filing_status == "Married Filing Jointly":
            if age_65_or_older and spouse_65_or_older:
                threshold = requirements["both_65_or_older"]
            elif age_65_or_older or spouse_65_or_older:
                threshold = requirements["one_65_or_older"]
            else:
                threshold = requirements["both_under_65"]
        else:  # Married Filing Separately
            threshold = requirements["any_age"]
        
        must_file = gross_income >= threshold
        
        # Additional reasons you might need to file even if below threshold
        special_circumstances = [
            "You had self-employment income over $400",
            "You owe special taxes (AMT, household employment taxes, etc.)",
            "You received advance payments of the Premium Tax Credit",
            "You owe taxes on a retirement plan distribution",
            "You received HSA or MSA distributions",
        ]
        
        # Reasons you might WANT to file even if not required
        reasons_to_file_anyway = [
            "You had federal income tax withheld from your pay",
            "You qualify for the Earned Income Tax Credit (EITC)",
            "You qualify for the Child Tax Credit",
            "You qualify for other refundable credits",
            "You made estimated tax payments",
        ]
        
        return {
            "must_file": must_file,
            "threshold": threshold,
            "gross_income": gross_income,
            "amount_over": gross_income - threshold if must_file else 0,
            "amount_under": threshold - gross_income if not must_file else 0,
            "special_circumstances": special_circumstances,
            "reasons_to_file_anyway": reasons_to_file_anyway,
        }

    def calculate_all_taxes(self, hourly_rate: float, hours_per_week: float,
                            filing_status: str, state: str,
                            age_65_or_older: bool = False,
                            spouse_65_or_older: bool = False) -> dict:
        weekly_gross = hourly_rate * hours_per_week
        annual_gross = weekly_gross * 52

        standard_deduction = self.standard_deductions[filing_status]
        taxable_income = max(0, annual_gross - standard_deduction)

        federal_tax, federal_breakdown = self.calculate_federal_tax(taxable_income, filing_status)

        ss_tax = min(annual_gross, self.fica["ss_cap"]) * self.fica["ss_rate"]
        medicare_tax = annual_gross * self.fica["medicare_rate"]

        state_rate = STATE_TAX_DATA.get(state, 0)
        state_tax = taxable_income * state_rate

        total_tax = federal_tax + ss_tax + medicare_tax + state_tax
        annual_take_home = annual_gross - total_tax
        total_hours = hours_per_week * 52

        # Check filing requirement
        filing_info = self.check_filing_requirement(
            annual_gross, filing_status, age_65_or_older, spouse_65_or_older
        )

        return {
            "hourly_rate": hourly_rate,
            "hours_per_week": hours_per_week,
            "weekly_gross": weekly_gross,
            "annual_gross": annual_gross,
            "standard_deduction": standard_deduction,
            "taxable_income": taxable_income,
            "federal_tax": federal_tax,
            "federal_breakdown": federal_breakdown,
            "ss_tax": ss_tax,
            "medicare_tax": medicare_tax,
            "state_tax": state_tax,
            "state_rate": state_rate,
            "total_tax": total_tax,
            "annual_take_home": annual_take_home,
            "monthly_take_home": annual_take_home / 12,
            "weekly_take_home": annual_take_home / 52,
            "hourly_take_home": annual_take_home / total_hours if total_hours > 0 else 0,
            "effective_rate": (total_tax / annual_gross * 100) if annual_gross > 0 else 0,
            "filing_info": filing_info,
        }


class TaxCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hourly Tax Calculator 2024/2025")
        self.root.geometry("750x750")
        self.root.configure(bg="#f5f5f5")
        self.calculator = TaxCalculator(2024)
        self.results = None
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = tk.Label(main_frame, text="Hourly Tax Calculator",
                         font=('Helvetica', 18, 'bold'), bg="#f5f5f5")
        title.pack(pady=(0, 20))

        input_frame = ttk.LabelFrame(main_frame, text="Enter Your Information", padding="15")
        input_frame.pack(fill="x", pady=10)

        # Tax Year
        ttk.Label(input_frame, text="Tax Year:").grid(row=0, column=0, sticky="w", pady=8)
        self.tax_year_var = tk.StringVar(value="2024")
        year_frame = ttk.Frame(input_frame)
        year_frame.grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(year_frame, text="2024", variable=self.tax_year_var, value="2024").pack(side="left", padx=5)
        ttk.Radiobutton(year_frame, text="2025", variable=self.tax_year_var, value="2025").pack(side="left", padx=5)

        # Hourly Rate
        ttk.Label(input_frame, text="Hourly Rate ($):").grid(row=1, column=0, sticky="w", pady=8)
        self.hourly_var = tk.StringVar(value="15.00")
        ttk.Entry(input_frame, textvariable=self.hourly_var, width=15).grid(row=1, column=1, sticky="w", pady=8)

        # Hours Per Week
        ttk.Label(input_frame, text="Hours Per Week:").grid(row=2, column=0, sticky="w", pady=8)
        self.hours_var = tk.StringVar(value="20")
        ttk.Entry(input_frame, textvariable=self.hours_var, width=15).grid(row=2, column=1, sticky="w", pady=8)

        # Filing Status
        ttk.Label(input_frame, text="Filing Status:").grid(row=3, column=0, sticky="w", pady=8)
        self.filing_var = tk.StringVar(value="Single")
        filing_combo = ttk.Combobox(input_frame, textvariable=self.filing_var, width=25, state="readonly",
                     values=["Single", "Married Filing Jointly", "Married Filing Separately", "Head of Household"])
        filing_combo.grid(row=3, column=1, sticky="w", pady=8)
        filing_combo.bind("<<ComboboxSelected>>", self.on_filing_status_change)

        # State
        ttk.Label(input_frame, text="State:").grid(row=4, column=0, sticky="w", pady=8)
        self.state_var = tk.StringVar(value="California")
        ttk.Combobox(input_frame, textvariable=self.state_var, width=25, state="readonly",
                     values=sorted(STATE_TAX_DATA.keys())).grid(row=4, column=1, sticky="w", pady=8)

        # Age 65 or older checkbox
        ttk.Label(input_frame, text="Age:").grid(row=5, column=0, sticky="w", pady=8)
        self.age_65_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(input_frame, text="I am 65 or older", variable=self.age_65_var).grid(row=5, column=1, sticky="w", pady=8)

        # Spouse age (only shown for Married Filing Jointly)
        self.spouse_age_label = ttk.Label(input_frame, text="Spouse Age:")
        self.spouse_65_var = tk.BooleanVar(value=False)
        self.spouse_age_check = ttk.Checkbutton(input_frame, text="Spouse is 65 or older", variable=self.spouse_65_var)
        
        # Initially hide spouse age option
        self.spouse_age_label.grid(row=6, column=0, sticky="w", pady=8)
        self.spouse_age_check.grid(row=6, column=1, sticky="w", pady=8)
        self.spouse_age_label.grid_remove()
        self.spouse_age_check.grid_remove()

        # Calculate Button
        calc_btn = tk.Button(main_frame, text="Calculate Taxes", command=self.calculate,
                             font=('Helvetica', 12, 'bold'), bg="#4CAF50", fg="white",
                             padx=30, pady=10, cursor="hand2")
        calc_btn.pack(pady=20)

        # Results Frame
        self.results_frame = ttk.LabelFrame(main_frame, text="Results", padding="15")
        self.results_frame.pack(fill="both", expand=True, pady=10)

        ttk.Label(self.results_frame, text="Enter your info and click Calculate").pack(pady=20)

    def on_filing_status_change(self, event=None):
        """Show/hide spouse age option based on filing status."""
        if self.filing_var.get() == "Married Filing Jointly":
            self.spouse_age_label.grid()
            self.spouse_age_check.grid()
        else:
            self.spouse_age_label.grid_remove()
            self.spouse_age_check.grid_remove()
            self.spouse_65_var.set(False)

    def calculate(self):
        try:
            hourly_rate = float(self.hourly_var.get())
            hours_per_week = float(self.hours_var.get())
            filing_status = self.filing_var.get()
            state = self.state_var.get()
            tax_year = int(self.tax_year_var.get())
            age_65_or_older = self.age_65_var.get()
            spouse_65_or_older = self.spouse_65_var.get()

            if hourly_rate <= 0 or hours_per_week <= 0:
                messagebox.showerror("Error", "Please enter positive values.")
                return

            self.calculator = TaxCalculator(tax_year)
            self.results = self.calculator.calculate_all_taxes(
                hourly_rate, hours_per_week, filing_status, state,
                age_65_or_older, spouse_65_or_older
            )
            self.display_results()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def display_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not self.results:
            return

        r = self.results
        f = r["filing_info"]

        canvas = tk.Canvas(self.results_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#ffffff")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Enable mousewheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Filing Requirement Banner
        filing_frame = tk.Frame(scroll_frame, bg="#d32f2f" if f["must_file"] else "#388e3c", padx=15, pady=12)
        filing_frame.pack(fill="x", pady=(0, 10))

        if f["must_file"]:
            filing_text = f"⚠️ YOU ARE REQUIRED TO FILE A TAX RETURN"
            filing_detail = f"Your gross income (${f['gross_income']:,.2f}) exceeds the filing threshold (${f['threshold']:,.2f}) by ${f['amount_over']:,.2f}"
        else:
            filing_text = f"✓ YOU ARE NOT REQUIRED TO FILE A TAX RETURN"
            filing_detail = f"Your gross income (${f['gross_income']:,.2f}) is below the filing threshold (${f['threshold']:,.2f}) by ${f['amount_under']:,.2f}"

        tk.Label(filing_frame, text=filing_text, font=('Helvetica', 11, 'bold'),
                 bg=filing_frame.cget('bg'), fg="white").pack()
        tk.Label(filing_frame, text=filing_detail, font=('Helvetica', 9),
                 bg=filing_frame.cget('bg'), fg="white").pack()

        # Summary Cards
        cards = tk.Frame(scroll_frame, bg="#ffffff")
        cards.pack(fill="x", pady=10, padx=5)

        for i, (title, value, color) in enumerate([
            ("Gross Annual", f"${r['annual_gross']:,.2f}", "#e3f2fd"),
            ("Total Taxes", f"${r['total_tax']:,.2f}", "#ffebee"),
            ("Take Home", f"${r['annual_take_home']:,.2f}", "#e8f5e9"),
            ("Eff. Rate", f"{r['effective_rate']:.1f}%", "#fff3e0")
        ]):
            card = tk.Frame(cards, bg=color, padx=12, pady=8)
            card.grid(row=0, column=i, padx=5, sticky="nsew")
            cards.grid_columnconfigure(i, weight=1)
            tk.Label(card, text=title, font=('Helvetica', 9), bg=color).pack()
            tk.Label(card, text=value, font=('Helvetica', 12, 'bold'), bg=color).pack()

        # Details Frame
        details = tk.Frame(scroll_frame, bg="#ffffff")
        details.pack(fill="x", pady=10, padx=10)

        data = [
            ("INCOME", None, None),
            ("Hourly Rate:", f"${r['hourly_rate']:.2f}/hr", "#333"),
            ("Hours/Week:", f"{r['hours_per_week']:.1f}", "#333"),
            ("Weekly Gross:", f"${r['weekly_gross']:,.2f}", "#333"),
            ("Annual Gross:", f"${r['annual_gross']:,.2f}", "#2e7d32"),
            ("", "", ""),
            ("DEDUCTIONS", None, None),
            ("Standard Deduction:", f"-${r['standard_deduction']:,.2f}", "#333"),
            ("Taxable Income:", f"${r['taxable_income']:,.2f}", "#333"),
            ("", "", ""),
            ("TAXES", None, None),
            ("Federal Tax:", f"${r['federal_tax']:,.2f}", "#c62828"),
            ("Social Security (6.2%):", f"${r['ss_tax']:,.2f}", "#c62828"),
            ("Medicare (1.45%):", f"${r['medicare_tax']:,.2f}", "#c62828"),
            (f"State Tax ({r['state_rate']*100:.2f}%):", f"${r['state_tax']:,.2f}", "#c62828"),
            ("TOTAL TAXES:", f"${r['total_tax']:,.2f}", "#c62828"),
            ("", "", ""),
            ("TAKE HOME", None, None),
            ("Annual:", f"${r['annual_take_home']:,.2f}", "#2e7d32"),
            ("Monthly:", f"${r['monthly_take_home']:,.2f}", "#2e7d32"),
            ("Weekly:", f"${r['weekly_take_home']:,.2f}", "#2e7d32"),
            ("Hourly (effective):", f"${r['hourly_take_home']:,.2f}/hr", "#2e7d32"),
        ]

        row_idx = 0
        for label, value, color in data:
            if value is None:
                tk.Label(details, text=label, font=('Helvetica', 11, 'bold'),
                         bg="#ffffff").grid(row=row_idx, column=0, columnspan=2, sticky="w", pady=(10, 5))
            elif label == "":
                row_idx += 1
                continue
            else:
                bold = label in ["Annual Gross:", "TOTAL TAXES:", "Hourly (effective):"]
                font = ('Helvetica', 10, 'bold') if bold else ('Helvetica', 10)
                tk.Label(details, text=label, font=font, bg="#ffffff").grid(row=row_idx, column=0, sticky="w", pady=2)
                tk.Label(details, text=value, font=font, bg="#ffffff", fg=color).grid(row=row_idx, column=1, sticky="e", pady=2)
            row_idx += 1

        # Filing Information Section
        filing_info_frame = tk.Frame(scroll_frame, bg="#f5f5f5", padx=10, pady=10)
        filing_info_frame.pack(fill="x", pady=10, padx=5)

        tk.Label(filing_info_frame, text="📋 FILING INFORMATION", font=('Helvetica', 11, 'bold'),
                 bg="#f5f5f5").pack(anchor="w")
        
        tk.Label(filing_info_frame, text=f"\nFiling Threshold for {self.tax_year_var.get()}: ${f['threshold']:,.2f}",
                 font=('Helvetica', 10), bg="#f5f5f5").pack(anchor="w")
        tk.Label(filing_info_frame, text=f"Your Gross Income: ${f['gross_income']:,.2f}",
                 font=('Helvetica', 10), bg="#f5f5f5").pack(anchor="w")

        # Special circumstances note
        if not f["must_file"]:
            tk.Label(filing_info_frame, text="\n⚠️ You may still need to file if:",
                     font=('Helvetica', 10, 'bold'), bg="#f5f5f5", fg="#e65100").pack(anchor="w")
            for item in f["special_circumstances"][:3]:
                tk.Label(filing_info_frame, text=f"  • {item}",
                         font=('Helvetica', 9), bg="#f5f5f5").pack(anchor="w")
            
            tk.Label(filing_info_frame, text="\n💡 You may want to file anyway if:",
                     font=('Helvetica', 10, 'bold'), bg="#f5f5f5", fg="#1976d2").pack(anchor="w")
            for item in f["reasons_to_file_anyway"][:3]:
                tk.Label(filing_info_frame, text=f"  • {item}",
                         font=('Helvetica', 9), bg="#f5f5f5").pack(anchor="w")

        # IRS Disclaimer
        disclaimer = tk.Label(scroll_frame, 
                             text="Source: IRS.gov - This is an estimate. Consult a tax professional for advice.",
                             font=('Helvetica', 8, 'italic'), bg="#ffffff", fg="#757575")
        disclaimer.pack(pady=10)


def main():
    root = tk.Tk()
    app = TaxCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()