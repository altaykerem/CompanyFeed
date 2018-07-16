class MailAdapter:
    file_writer = None

    def open_file(self, file_str):
        self.file_writer = open(file_str, "a")

    def close_file(self):
        self.file_writer.close()

    def open_table(self, title, columns_num):
        open_table = """
        <tr>
            <td bgcolor="#ffffff">
                <table border="1" cellpadding="0" cellspacing="0" width="100%%">
                    <tr>"""
        self.file_writer.write(open_table)
        self.file_writer.write("<td colspan=\""+str(columns_num)+"\"><h3 align=\"center\">")
        self.file_writer.write(title)
        self.file_writer.write(" </h3></td></tr>")

    def close_table(self):
        self.file_writer.write("</table></td></tr>")

    def open_row(self):
        self.file_writer.write("<tr>\n")
        self.file_writer.write("<td> <table width=\"100%\" style=\"border-spacing: 20px;\">\n")

    def close_row(self):
        self.file_writer.write("</table></td></tr>\n")

    # Add after a row, spans all columns
    def add_header_data(self, content, columns_num):
        self.file_writer.write("<tr><td colspan=\""+str(columns_num)+"\" align=\"center\">")
        self.file_writer.write(content+"</td></tr>\n")

    def add_row_data(self, column_contents):
        self.file_writer.write("<tr>\n")
        for content in column_contents:
            self.file_writer.write("<td colspan=\"1\" align=\"center\">" + content + "</td>\n")
        self.file_writer.write("</tr>\n")

    def adapt_image(self, url):
        self.file_writer.write("<img src=\"" + url + "\" style=\"height:126px;border:0;\">")

    @staticmethod
    def make_bold(s):
        return "<b>"+s+"</b>"

    @staticmethod
    def underline(s):
        return "<u>"+s+"</u>"
