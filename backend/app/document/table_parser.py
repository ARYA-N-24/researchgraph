import os
import camelot

from app.config import settings


class TableParser:

    """
    Extract tables from PDFs
    and convert to text chunks.
    """

    def __init__(self):

        self.documents_dir = (
            settings.DOCUMENTS_DIR
        )

        self.tables_dir = (
            settings.TABLES_DIR
        )

        os.makedirs(
            self.tables_dir,
            exist_ok=True
        )


    def extract_tables_from_pdf(
        self,
        pdf_path
    ):

        table_chunks = []

        try:

            tables = camelot.read_pdf(
                pdf_path,
                pages="all",
                flavor="lattice"
            )

            print(
                f"📊 Found {tables.n} tables in {pdf_path}"
            )

            for i, table in enumerate(tables):

                df = table.df

                csv_path = os.path.join(

                    self.tables_dir,

                    f"{os.path.basename(pdf_path)}_table_{i}.csv"

                )

                df.to_csv(
                    csv_path,
                    index=False
                )

                table_text = df.to_string()

                table_chunks.append({

                    "content":
                    f"Table from {pdf_path}\n{table_text}",

                    "metadata": {

                        "source": csv_path,

                        "type": "table"

                    }

                })

        except Exception as e:

            print(
                f"⚠️ Table extraction error: {e}"
            )

        return table_chunks


    def extract_all_tables(self):

        all_tables = []

        for file in os.listdir(
            self.documents_dir
        ):

            if file.endswith(".pdf"):

                pdf_path = os.path.join(
                    self.documents_dir,
                    file
                )

                tables = (

                    self.extract_tables_from_pdf(
                        pdf_path
                    )

                )

                all_tables.extend(
                    tables
                )

        print(
            f"📊 Total tables extracted: {len(all_tables)}"
        )

        return all_tables