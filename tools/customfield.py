# parse custom field information from the rule

import PySimpleGUI as sg
import pyperclip
import re
							

class CustomField:

	def main(self):

		layout = [
			[sg.Text('sourceTable'), sg.Text(' '*49), sg.Text('sourceTableRowId')
			,sg.Text('linkingId'), sg.Text(' '*11), sg.Text('linkingIdSeq')
			,sg.Text('linkingIdSourceTable')],
			[sg.Input(size=(40, 1), key='sourceTable'), sg.Input(size=(15, 1), key='sourceTableRowId')
			,sg.Input(size=(15, 1), key='linkingId'), sg.Input(size=(10, 1), key='linkingIdSeq')
			,sg.Input(size=(40, 1), key='linkingIdSourceTable')],
			[sg.Text('Custom Field Rule')],
			[sg.Multiline(size=(140, 5), key='rule')],

			[sg.Button('Parse')],

			[sg.Text('customFieldData:    ', key='colname', size=(100,1))],
			[sg.Text('parentType:         ', key='fieldtype', size=(100,1))],
			[sg.Text('fieldDisplayName:   ', key='fieldname', size=(100,1))],
			[sg.Text('fieldDisplayType:   ', key='displaytype', size=(100,1))],
			[sg.Text('parseDelimiter:     ', key='delimiter', size=(100,1))],
			[sg.Text('fieldGroupName:     ', key='group', size=(100,1))],

			[sg.Multiline(size=(140, 5), key='sql')],
			[sg.Button('Copy')]
		]

		window = sg.Window(title='Custom Filed Rule Parser', layout=layout)

		for i in range(1000000):
			event, values = window.read()
			if event is None:
				break

			if event == 'Parse':
				rule = values['rule'].strip()

				if rule == '':
					continue

				# parse column name
				if ':' not in rule:
					sg.Popup('Failed to parse column name')
					continue

				colname = rule.split(':')[0]
				colname = re.sub(r'^[^a-z0-9].Column [A-Z]{1,2}', '', colname)
				colname = colname.strip(' \n-,()')
				colname = '`' + colname + '`'

				# parse custom field type
				rule_lower = ':'.join(rule.lower().split(':')[1:])
				if 'custom field' not in rule_lower:
					sg.Popup('Failed to parse custom field')
					continue
				fieldtype = rule_lower.split('custom field')[0].strip()
				fieldtype = fieldtype.split(' ')[-1]
				if 'account' in fieldtype:
					fieldtype = 'account_custom_data'
				elif 'individual' in fieldtype:
					fieldtype = 'user_custom_data'
				elif 'company' in fieldtype:
					fieldtype = 'company_custom_data'
				elif 'activity' in fieldtype:
					fieldtype = 'contact_activity_custom_data'
				elif 'donation' in fieldtype:
					fieldtype = 'donation_custom_data'
				elif 'attendee' in fieldtype:
					fieldtype = 'event_attendee_custom_data'
				elif 'registration' in fieldtype:
					fieldtype = 'event_registration_custom_data'
				elif 'membership' in fieldtype:
					fieldtype = 'membership_listing_custom_data'
				elif 'product' in fieldtype:
					fieldtype = 'product_custom_data'
				else:
					sg.Popup('Failed to parse parentType')
					fieldtype = 'NULL'

				# parse field display type
				if 'radio' in rule_lower:
					displaytype = 'R'
				elif re.search(r'check[ -]?box', rule_lower):
					displaytype = 'C'
				elif re.search(r'drop[ -]?down', rule_lower):
					displaytype = 'D'
				elif re.search(r'multi(ple)? ?-? ?line( text)?', rule_lower):
					displaytype = 'M'
				else:
					displaytype = 'O'

				# parse field display name
				fieldname = re.split('custom field', rule, flags=re.I)[1]
				fieldname = fieldname.replace('”', '"').replace('“', '"')
				if re.search('".*?"', fieldname):
					fieldname = re.split('"', fieldname, flags=re.I)[1]
				else:
					fieldname = colname.strip('`')

				# parse delimiter
				if re.search('custom field.*?separate', rule, flags=re.I):
					delimiter = re.split('separate', rule, flags=re.I)[1]
					if 'comma' in delimiter or '","' in delimiter:
						delimiter = ','
					elif 'semicolon' in delimiter or '";"' in delimiter:
						delimiter = ';'
					elif 'slash' in delimiter in delimiter or '"/"':
						delimiter = '/'
					else:
						delimiter = 'NULL'
				else:
					delimiter = 'NULL'

				# parse group
				group = re.split('custom field group', rule, flags=re.I)
				if len(group) > 1:
					group = group[1]
					group = group.replace('”', '"').replace('“', '"')
					if re.search('".*?"', group):
						group = re.split('"', group, flags=re.I)[1]
					else:
						group = 'NULL'
				else:
					group = 'NULL'

				l = ["'", "'"]
				sql = 'SELECT ' + values['sourceTable'].join(l) + ',' + values['sourceTableRowId'] + ',' \
						+ values['linkingId'] + ',' + values['linkingIdSeq'] + ',' + values['linkingIdSourceTable'].join(l) \
						+ ',' + colname + ',' + fieldtype.join(l) + ',' + fieldname.join(l) + ',' + group.join(l) + ',' + displaytype.join(l) + ',' \
						+ delimiter.join(l)\
						+ ' FROM ' + values['sourceTable']\
						+ ' WHERE ' + colname + ' IS NOT NULL \nUNION ALL'

				sql = sql.replace(",'NULL'", ',NULL')
				window['sql'].update(sql)
				window['colname'].update('customFieldData:    '+colname)
				window['fieldtype'].update('parentType:         '+fieldtype)
				window['fieldname'].update('fieldDisplayName:   '+fieldname)
				window['displaytype'].update('fieldDisplayType:     '+displaytype)
				window['delimiter'].update('parseDelimiter:     '+delimiter)
				window['group'].update('fieldGroupName:     '+group)

			if event == 'Copy':
				sql = values['sql'].strip()+'\n'
				pyperclip.copy(sql)

		window.close()


if '__name__' == '__main__':
	CustomField = CustomField()
	CustomField.main()