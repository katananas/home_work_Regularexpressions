from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

def merged_contact(contact_list):
  pattern_number = r"(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})"
  pattern_additional_number = r"\s*\(*(доб.)\s*(\d*)\)*\s*"
  pattern_name = (r"(^([А-я]+)\s([А-я]+)\s([А-я]+)\,\,)"
                  r"|(^([А-я]+)\,([А-я]+)\,([А-я]+))"
                  r"|(^([А-я]+)\s([А-я]+)(\,)\,)"
                  r"|(^([А-я]+)\,([А-я]+)\s([А-я]+)\,)")

  str_line = ','.join(contact_list)
  str_line = re.sub(pattern_name, r"\2\6\10\14,\3\7\11\15,\4\8\16", str_line)
  str_line = re.sub(pattern_number, r"+7(\2)\3-\4-\5", str_line)
  str_line = re.sub(pattern_additional_number, r" \1\2", str_line)
  return str_line.split(',')

update_contacts_list = []
for contact in contacts_list:
    update_contacts_list.append(merged_contact(contact))

finish_contacts_list = []
contacts_list_length = len(update_contacts_list)

dubl_records = []

# объединяем дубли

for i in range(contacts_list_length - 1):
    if i in dubl_records:
        continue
    contact = update_contacts_list[i]
    for j in range(i + 1, len(update_contacts_list)):
        if contact[0] == update_contacts_list[j][0] and contact[1] == update_contacts_list[j][1]:
            dubl_records.append(j)
            contact = [contact[_] if contact[_] != "" else update_contacts_list[j][_]
                       for _ in range(len(contact))]
    finish_contacts_list.append(contact)

# код записи файла в формате CSV

with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(finish_contacts_list)