def cov_source_for_test_paths(paths):
	'''Given test paths, return the source paths on which to measure
	the coverage. If no specific test paths were given, measure coverage on
	entier Python code tree.'''
	if not paths:
		return ['code']
	return [_code_path(p) for p in paths]

def _code_path(path):
	'''Returns the code path corresponding to a given test path.'''
	return path.replace('tests/', 'clue/').replace('test_', '')