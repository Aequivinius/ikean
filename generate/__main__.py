from generate.generator import Generator


generator = Generator()
for template, type in generator.page_types.items():
    generator.generate(template, type == "checkerboard")
