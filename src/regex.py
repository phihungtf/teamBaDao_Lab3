import re

raw = [
  "Dihydro Artemisinin 80 mg, Piperaquine phosphate 640 mg",
  "Fentanyl critrate",
  "Bisoprolol fumarat 5mg",
  "Rabeprazole natri ",
  "Fursulthiamin 50 mg, Pyridoxin HCl 250 mg, Methylcobalamin 0,50 mg",
  "Fluoxetin (dưới dạng Fluoxetin hydroclorid) ",
  "Etodolac",
  "Dextromethorphan hydrobromid; Terpin hydrat , Natri benzoat ",
  "Fentanil (dưới dạng fentanil citrate) ",
  " Esomeprazol ",
  "Paracetamol 500 mg; Codein phosphat hemihydrat 15 mg",
  "Hoàng bá",
  "Mỗi viên chứa: L-leucin 18,3mg; L-isoleucin 5,9mg; Lysin HCl 25mg; L-phenylalanin 5mg; L-threonin 4,2mg; L-valin 6,7mg; L-tryptophan 5mg; L-methionin 18,4mg; 5-hydroxyanthranilic acid HCl 0,2mg; Vitamin A 2000IU; Vitamin D2 200IU; Vitamin B1 5mg; Vitamin B2 3mg; Nicotinamid 20mg; Vitamin B6 2,5mg; Acid folic 0,2mg; Calci pantothenat 5mg; Vitamin B12 1mcg; Vitamin C 20mg; Vitamin E 1mg",
  "Oxycodon HCl; Naloxon HCl ",
  "Artemether 40mg; Lumefantrin 240mg",
  "Trimetazidin hydroclorid ",
  "Atropine sulfate. H2O",
  "Xa tiền tử ; Nhục quế ; Hoài sơn ; Cao đặc các dược liệu (tương đương với Thục địa ; Sơn thù ; Phục linh; Mẫu đơn bì ; Trạch tả ; Ngưu tất ; Phụ tử chế ) ",
  " Cefotaxim natri",
  "Everolimus 5mg"
]

class APIRegexHelper:
	def __init__(self, string):
		self.string = string
		
	# remove mass and unit
	def remove_mass_and_unit(self):
		# remove mass
		self.string = re.sub(r'\d+((,|\.)\d+)*\s*(mg|mcg|IU|UI|g|ml|l|kg|mm|\%)', '', self.string)
		return self

	# remove leading and trailing spaces
	def remove_space(self):
		self.string = self.string.strip()
		return self

	# remove all the string after the first parenthesis
	def remove_parenthesis(self):
		self.string = re.sub(r'(\(|\)).*', '', self.string)
		return self
	
	# remove all the slash
	def remove_slash(self):
		self.string = re.sub(r'\s*/', '', self.string)
		return self
	
	# remove similar strings
	def remove_similar_string(self):
		self.string = re.sub(r'(tương đương|tương ứng).*', '', self.string)
		return self

	# remove all the string before the first colon
	def remove_colon(self):
		self.string = re.sub(r'.*:', '', self.string)
		return self

class UltimateAPIRegex:
	def __init__(self, string):
		self.string = string
		self.apis = []
		
	def get_apis(self):
		# split by comma or semicolon that not followed by digit
		temp_list = re.split(r'(,|;)\s*(?![0-9])', self.string)
		for s in temp_list:
			temp = APIRegexHelper(s) \
					.remove_mass_and_unit() \
			 		.remove_parenthesis() \
			 		.remove_colon() \
			 		.remove_similar_string() \
			 		.remove_slash() \
			 		.remove_space()
			self.apis.append(temp.string)
		self.remove_incorrect_string()
		return self.apis
	
	# remove incorrect strings
	def remove_incorrect_string(self):
		incorrect_strings = [';', '(', ')', ':', '', ' ', ',']
		self.apis = [s for s in self.apis if s not in incorrect_strings]

api_list = []
for s in raw:
	api = UltimateAPIRegex(s)
	api_list.append(api.get_apis())

print(api_list)

# q: what is the meaning of this regex: ^(?=.*\d)(?=.*\bvitamin\b)|^(?!\d).*$
# a: it means that the string must contain at least one digit and the word vitamin or the string must not contain any digit
# q: how to change the regex to also match the string format: 2,4-Dichlorophenoxyacetic acid
# a: ^(?=.*\d)(?=.*\bvitamin\b)|^(?!\d).*|^(?=.*\d)(?=.*\b[a-z]\b).*$
