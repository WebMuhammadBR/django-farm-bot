import pandas as pd
from io import BytesIO


async def farmers_to_excel(data: list):
    """
    Фермерлар рўйхатини Excel файлига айлантиради.
    data -> API дан келган list[dict]
    """

    if not data:
        return None

    # Керакли колонкаларни тайёрлаймиз
    formatted = []

    for index, farmer in enumerate(data, start=1):
        formatted.append({
            "№": index,
            "ИНН": farmer["inn"],
            "Фермер номи": farmer["name"],
            "Баланс": float(farmer["balance"]),
        })

    df = pd.DataFrame(formatted)

    buffer = BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)

    return buffer


import pandas as pd
from io import BytesIO
from openpyxl.styles import Font


async def contracts_to_excel(data: list):

    if not data:
        return None

    formatted = []

    for index, item in enumerate(data, start=1):
        formatted.append({
            "№": index,
            "Вилоят": item["region"],
            "Туман": item["district"],
            "Массив": item["massive"],
            "Фермер": item["name"],
            "Миқдор (тн)": float(item["quantity"]),
            "Сумма": float(item["amount"]),
        })

    df = pd.DataFrame(formatted)

    buffer = BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Contracts")

        worksheet = writer.sheets["Contracts"]

        # 🔥 HEADER BOLD
        for cell in worksheet[1]:
            cell.font = Font(bold=True)

        # 🔥 AUTO WIDTH
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass

            adjusted_width = max_length + 2
            worksheet.column_dimensions[column_letter].width = adjusted_width

    buffer.seek(0)
    return buffer














"""for index, item in enumerate(data, start=1):
        formatted.append({
            "№": index,
            "Вилоят": item["region"],
            "Туман": item["district"],
            "Массив": item["massive"],
            "Фермер": item["name"],
            "Миқдор (тн)": float(item["quantity"]),
            "Сумма": float(item["amount"]),
        })"""