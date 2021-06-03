import base64


file4_ = open("amazon.png", "rb")
contents = file4_.read()
file_amazon_url = base64.b64encode(contents).decode("utf-8")
file4_.close()

def make_content_string(df):
	if len(df) < 3:
		content_html_str = '''
<p style="color: red;margin-top:100px">Sorry! Zu deinen Filtereinstellungen passen weniger als drei Eintraege.</p>'''
		return(content_html_str)
	else:
		string_tuple = make_string_tuple(df,0) + make_string_tuple(df,1) + make_string_tuple(df,2)
		content_html_str =	'''
<div style="color:#bbbbbb">
<p style="font-size:40px; height:110px"> <span style="float:left;font-size:75px;top:-14px; position: relative; margin-right: 20px">1.</span>  
%s<br> <span style="position:relative; font-size: 0.4em; font-style:italic; top:-35px">%s</span>
</p>
<p style="clear:left; position:relative; top:-35px; padding-left:5px"><b>Regisseur:</b> %s &nbsp; | &nbsp; <b>Laufzeit:</b> %s</b> &nbsp; | &nbsp; <a href="%s" target = "_blank">Auf Amazon finden</a>  </p>
</div>

<div style="color:#bbbbbb; margin-top:-10px">
<p style="font-size:40px; height:110px"> <span style="float:left;font-size:75px;top:-14px; position: relative; margin-right: 20px">2.</span>  
%s<br> <span style="position:relative; font-size: 0.4em; font-style:italic; top:-35px">%s</span>
</p>
<p style="clear:left; position:relative; top:-35px; padding-left:5px"><b>Regisseur:</b> %s &nbsp; | &nbsp; <b>Laufzeit:</b> %s</b> &nbsp; | &nbsp; <a href="%s" target = "_blank">Auf Amazon finden</a>  </p>
</div>

<div style="color:#bbbbbb; margin-top:-10px">
<p style="font-size:40px; height:110px"> <span style="float:left;font-size:75px;top:-14px; position: relative; margin-right: 20px">3.</span>  
%s<br> <span style="position:relative; font-size: 0.4em; font-style:italic; top:-35px">%s</span>
</p>
<p style="clear:left; position:relative; top:-35px; padding-left:5px"><b>Regisseur:</b> %s &nbsp; | &nbsp; <b>Laufzeit:</b> %s</b> &nbsp; | &nbsp; <a href="%s" target = "_blank">Auf Amazon finden</a>  </p>
</div>''' % string_tuple

		if len(df) > 3:
			content_html_str = content_html_str + '<hr style="margin-top:-10px" >\n<div>\n<p style="color:#bbbbbb; margin-left:5px; line-height:26px">\n'
			for nr in range(3,len(df)):
				content_html_str = content_html_str + f'<b> {nr+1}.</b> {df.iloc[nr,:]["title"]}  |   <a href="{df.iloc[nr,:]["amazon_link"]}" target = "_blank">Auf Amazon finden</a> <br>\n'

			content_html_str = content_html_str + "</p>\n</div>"


	## Amazon Icon
	content_html_str = content_html_str.replace("Auf Amazon finden",f'<img style="margin-top:2px" src="data:image/gif;base64,{file_amazon_url}" width="20px"> auf Amazon finden ')

	return(content_html_str)


def make_string_tuple(df,row_number):
	df_row = df.iloc[row_number,:]
	title = df_row["title"]
	if (len(title) > 31):
		title = title[0:29] + "..."
	runtime = str(int(df_row["runtime"])) + " min"
	director =", ".join( df_row["director"])
	amazon_link = df_row["amazon_link"]
	tagline = df_row["tagline"] if df_row["tagline"] != "" else "This movie doesn't need a tagline"
	if (len(tagline) > 89):
		tagline = tagline[0:80] + "..."
	return((title,tagline,director,runtime,amazon_link))
