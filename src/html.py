import string


class HTML:
    def __init__(self, template_path):
        file = open(template_path)
        self.template = file.read()
        file.close()

    def __build_row(self, item) -> string:
        row = ""
        row += "<tr>"
        row += '<td><a href="%s">%s</a></td>' % (item["ipk"], item["Package"])
        row += '<td>%s</td>' % (item["Architecture"] or '')
        row += '<td>%s</td>' % (item["Version"] or '')
        row += '<td>%s</td>' % (item["Description"] or '')
        row += "</tr>"

        return row

    def write(self, target_path, items) -> None:
        rows = ""
        for item in items:
            rows += self.__build_row(item)

        html = self.template
        html = html.replace("{%ROWS%}", rows)

        file = open(target_path, "w")
        file.write(html)
        file.close()
