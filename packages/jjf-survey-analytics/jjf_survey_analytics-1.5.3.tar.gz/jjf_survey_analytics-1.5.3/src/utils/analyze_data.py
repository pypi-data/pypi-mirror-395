#!/usr/bin/env python3
"""
Data Analysis Script for Surveyor Database

Analyzes the extracted survey data and creates normalized tables
for better data structure and analysis.
"""

import json
import sqlite3
from collections import defaultdict


class DataAnalyzer:
    """Analyzes and normalizes the extracted survey data."""

    def __init__(self, db_path: str = "surveyor_data.db"):
        self.db_path = db_path

    def analyze_data_structure(self):
        """Analyze the structure of the extracted data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print("🔍 Analyzing Data Structure")
        print("=" * 40)

        # Get all raw data
        cursor.execute("SELECT data_json FROM raw_data")
        rows = cursor.fetchall()

        if not rows:
            print("❌ No data found in database")
            return

        # Analyze column structure
        all_columns = set()
        column_patterns = defaultdict(int)

        for row in rows:
            data = json.loads(row[0])
            columns = list(data.keys())
            all_columns.update(columns)

            # Count column patterns
            pattern = tuple(sorted(columns))
            column_patterns[pattern] += 1

        print(f"📊 Total rows analyzed: {len(rows)}")
        print(f"📋 Unique columns found: {len(all_columns)}")
        print(f"🔄 Column patterns: {len(column_patterns)}")

        print("\n📝 All columns:")
        for col in sorted(all_columns):
            print(f"  • {col}")

        # Show most common column pattern
        most_common_pattern = max(column_patterns.items(), key=lambda x: x[1])
        print(f"\n📈 Most common column pattern ({most_common_pattern[1]} rows):")
        for col in sorted(most_common_pattern[0]):
            print(f"  • {col}")

        conn.close()

    def analyze_survey_questions(self):
        """Analyze the survey questions and structure."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print("\n📋 Survey Questions Analysis")
        print("=" * 40)

        cursor.execute("SELECT data_json FROM raw_data ORDER BY row_number")
        rows = cursor.fetchall()

        questions = []
        for row in rows:
            data = json.loads(row[0])

            question_info = {
                "id": data.get("Question ID", ""),
                "question": data.get("QUESTION", ""),
                "answers": [],
            }

            # Extract answer options
            for i in range(1, 8):  # Answer 1 through Answer 7
                answer_key = f"Answer {i}"
                if answer_key in data and data[answer_key].strip():
                    question_info["answers"].append(data[answer_key])

            questions.append(question_info)

        print(f"📊 Total questions: {len(questions)}")

        # Show question types
        question_types = defaultdict(int)
        for q in questions:
            if not q["question"].strip():
                question_types["Empty/Comment"] += 1
            elif len(q["answers"]) > 3:
                question_types["Multiple Choice"] += 1
            elif len(q["answers"]) == 0:
                question_types["Open Text"] += 1
            else:
                question_types["Short Answer"] += 1

        print("\n📈 Question types:")
        for qtype, count in question_types.items():
            print(f"  • {qtype}: {count}")

        # Show sample questions
        print("\n📝 Sample questions:")
        for i, q in enumerate(questions[:5]):
            if q["question"].strip():
                print(f"\n  {i+1}. ID: {q['id']}")
                print(f"     Q: {q['question'][:100]}{'...' if len(q['question']) > 100 else ''}")
                print(f"     Answers: {len(q['answers'])}")

        conn.close()
        return questions

    def create_normalized_tables(self):
        """Create normalized tables for better data structure."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print("\n🏗️  Creating Normalized Tables")
        print("=" * 40)

        # Create questions table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT UNIQUE NOT NULL,
                question_text TEXT NOT NULL,
                question_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Create answer_options table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT NOT NULL,
                option_number INTEGER NOT NULL,
                option_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (question_id)
            )
        """
        )

        # Create survey_responses table (for future response data)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS survey_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                response_id TEXT NOT NULL,
                question_id TEXT NOT NULL,
                answer_value TEXT,
                answer_option_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (question_id) REFERENCES questions (question_id),
                FOREIGN KEY (answer_option_id) REFERENCES answer_options (id)
            )
        """
        )

        # Clear existing normalized data
        cursor.execute("DELETE FROM answer_options")
        cursor.execute("DELETE FROM questions")

        # Get questions data
        questions = self.analyze_survey_questions()

        # Insert questions and answers
        for q in questions:
            if not q["question"].strip():
                continue

            # Determine question type
            if len(q["answers"]) > 3:
                qtype = "multiple_choice"
            elif len(q["answers"]) == 0:
                qtype = "open_text"
            else:
                qtype = "short_answer"

            # Insert question
            cursor.execute(
                """
                INSERT OR REPLACE INTO questions (question_id, question_text, question_type)
                VALUES (?, ?, ?)
            """,
                (q["id"], q["question"], qtype),
            )

            # Insert answer options
            for i, answer in enumerate(q["answers"], 1):
                cursor.execute(
                    """
                    INSERT INTO answer_options (question_id, option_number, option_text)
                    VALUES (?, ?, ?)
                """,
                    (q["id"], i, answer),
                )

        conn.commit()

        # Show results
        cursor.execute("SELECT COUNT(*) FROM questions")
        question_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM answer_options")
        option_count = cursor.fetchone()[0]

        print("✅ Created normalized tables:")
        print(f"  • Questions: {question_count}")
        print(f"  • Answer options: {option_count}")

        conn.close()

    def show_database_schema(self):
        """Show the complete database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print("\n🗄️  Database Schema")
        print("=" * 40)

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            print(f"\n📋 Table: {table_name}")

            # Get table info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            for col in columns:
                col_id, name, col_type, not_null, default, pk = col
                pk_str = " (PRIMARY KEY)" if pk else ""
                not_null_str = " NOT NULL" if not_null else ""
                default_str = f" DEFAULT {default}" if default else ""
                print(f"  • {name}: {col_type}{not_null_str}{default_str}{pk_str}")

            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  📊 Rows: {count}")

        conn.close()

    def export_summary_report(self):
        """Export a summary report of the data."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        print("\n📊 Summary Report")
        print("=" * 40)

        # Extraction job summary
        cursor.execute(
            """
            SELECT job_name, status, processed_spreadsheets, total_rows, started_at, completed_at
            FROM extraction_jobs
            ORDER BY started_at DESC
            LIMIT 1
        """
        )

        job = cursor.fetchone()
        if job:
            name, status, processed, total, started, completed = job
            print("🔄 Latest extraction job:")
            print(f"  • Name: {name}")
            print(f"  • Status: {status}")
            print(f"  • Spreadsheets processed: {processed}")
            print(f"  • Total rows: {total}")
            print(f"  • Started: {started}")
            print(f"  • Completed: {completed}")

        # Question summary
        cursor.execute(
            """
            SELECT question_type, COUNT(*) as count
            FROM questions
            GROUP BY question_type
            ORDER BY count DESC
        """
        )

        qtypes = cursor.fetchall()
        if qtypes:
            print("\n📋 Question types:")
            for qtype, count in qtypes:
                print(f"  • {qtype}: {count}")

        # Sample questions
        cursor.execute(
            """
            SELECT q.question_id, q.question_text, COUNT(a.id) as option_count
            FROM questions q
            LEFT JOIN answer_options a ON q.question_id = a.question_id
            GROUP BY q.question_id, q.question_text
            ORDER BY option_count DESC
            LIMIT 5
        """
        )

        samples = cursor.fetchall()
        if samples:
            print("\n📝 Sample questions (with most options):")
            for qid, text, options in samples:
                print(
                    f"  • {qid}: {text[:80]}{'...' if len(text) > 80 else ''} ({options} options)"
                )

        conn.close()


def main():
    """Main function to run the data analysis."""
    print("📊 Surveyor Data Analysis")
    print("=" * 30)

    analyzer = DataAnalyzer()

    try:
        # Analyze data structure
        analyzer.analyze_data_structure()

        # Analyze survey questions
        analyzer.analyze_survey_questions()

        # Create normalized tables
        analyzer.create_normalized_tables()

        # Show database schema
        analyzer.show_database_schema()

        # Export summary report
        analyzer.export_summary_report()

        print("\n✅ Analysis completed successfully!")
        print("💾 Database: surveyor_data.db")

    except Exception as e:
        print(f"\n❌ Analysis failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
