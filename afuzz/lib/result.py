import os
import json
from urllib.parse import urlparse
from prettytable import PrettyTable
import pandas as pd

class FuzzResult:

    def __init__(self, *args, **kwargs):
        self.target = args[0]
        self.result = []
        self._result = []
        self.table = PrettyTable()
        self.table.title = self.target
        self.save_filename = self.target.replace(":", "_").replace("/", "_")
        self.last_result = {"result": [], "total": 0, "target": self.target}
        self.opt_output = args[1]
        self.fullpath = args[2]

        if self.fullpath:
            self.table.field_names = ["url", "status", "redirect", "title", "length", "content-type", "lines",
                                      "words", "type", "mark"]
        else:
            self.table.field_names = ["target", "path", "status", "redirect", "title", "length", "content-type", "lines",
                                      "words", "type", "mark"]

        # self.row_title = ["target","path","status","title","length","lines","words","type","mark"]

    def add(self, response, path, find_type, mark, target=None, depth=0):
        title = response.page_title()
        lines = response.lines
        words = response.words
        status = str(response.status)

        subdomain = urlparse(target).netloc.split(":", 1)[0]
        url = target + path
        if url not in self._result:
            self._result.append(url)
            if "application/" in response.type and "application/json" not in response.type:
                length = response.length
            else:
                length = len(response.clean_page())

            self.result.append(
                {
                    "target": target,
                    "path": path,
                    "status": response.status,
                    "redirect": response.redirect,
                    "title": title,
                    "length": length,
                    "content_type": response.type,
                    "lines": lines,
                    "words": words,
                    "type": find_type,
                    "mark": mark,
                    "subdomain": subdomain,
                    "depth": depth,
                    "url": url
                }
            )

    def output(self):
        if self.last_result["total"] > 0:
            print(self.table)

    def save(self):
        folder = "/".join(self.opt_output.split("/")[:-1])
        if not os.path.exists(folder):
            try:
                os.mkdir(folder)
            except:
                print("mkdir error")
                #return False
        if self.last_result["total"] > 0:
            with open("%s.json" % self.opt_output, "w", encoding="utf-8") as save_file:
                save_file.write(json.dumps(self.last_result))

    def save_table(self):
        if not os.path.exists(self.output):
            try:
                os.mkdir(self.output)
            except:
                print("mkdir error")
                return False
        if self.last_result["total"] > 0:
            with open("%s_%d.txt" % (self.output+"/"+self.save_filename, self.last_result["total"]), "w", encoding="utf-8") \
                    as save_file:
                save_file.write(self.target + "\n")
                save_file.write(self.table.get_string())

    def analysis(self):
        print("\nStart analyzing scan results...")
        result_list = self.result
        if result_list:
            result_df = pd.DataFrame(result_list)
            total = len(result_list)
            if total > 20:

                data_group = result_df.groupby(['type', 'status', 'length', 'lines'])
                for dp, value in data_group.groups.items():
                    #print(dp)
                    find_type, status, length, lines = dp
                    dp_len = len(value)

                    prefect = dp_len / total * 100
                    if dp_len < 20:
                        rows = result_df[(result_df["type"] == find_type) & (result_df["status"] == status) & (
                                length == result_df["length"])]
                        for index, row in rows.iterrows():
                            total = total - 1
                            print(row)
                            row_list = row.to_list()
                            if self.fullpath:
                                self.table.add_row([row_list[-1]] + row_list[2:11])
                            else:
                                self.table.add_row(row.to_list()[0:-3])
                            #self.table.add_row(row.to_list()[0:-3])
                            self.last_result["result"].append(row.to_dict())

            else:
                # ["path", "redirect", "status", "title", "length","content-type", "lines", "words", "type", "mark"]
                for data in result_list:

                    if self.fullpath:
                        self.table.add_row([data["url"], data["status"], data["redirect"], data["title"],
                                            data["length"], data["content_type"], data["lines"], data["words"],
                                            data["type"], data["mark"]])
                    else:
                        self.table.add_row(
                            [data["target"], data["path"], data["status"], data["redirect"], data["title"],
                             data["length"], data["content_type"], data["lines"], data["words"],
                             data["type"], data["mark"]])

                self.last_result["result"] += result_list
            self.last_result["total"] = len(self.last_result["result"])
        print("Results analysis complete!")
    #If the records in the remaining results are still greater than 20 after grouping, judge and filter. Only how much is kept.