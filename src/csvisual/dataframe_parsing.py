import pandas as pd

def generate_html(df: pd.DataFrame) -> tuple:
	columns = df.columns

	columns_html: str = ""
	row_html: str = ""

	for col in columns:
		columns_html += '<th scope="col"><script type="text/plain">%s</script></th>' % col
		# script tags in order to stop certain text rendering as actual html

	for _ , row in df.iterrows():
		row_html += "<tr>"
		for col in columns:
			row_html += '<td><script type="text/plain">%s</script></td>' % row[col]
		row_html += "</tr>"
		
	return (columns_html, row_html)