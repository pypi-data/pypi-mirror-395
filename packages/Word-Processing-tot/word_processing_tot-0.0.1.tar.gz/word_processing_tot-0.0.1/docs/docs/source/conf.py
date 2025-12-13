import os
import sys
# 소스 코드 위치를 Sphinx에게 알려줌
sys.path.insert(0, os.path.abspath('../../src'))

project = 'Word Frequency Lib'
copyright = '2025, Team Name'
author = 'Team Name'
release = '0.1.0'

# 사용할 확장 기능 (자동 문서화, Google 스타일 지원 등)
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = []

# 테마 설정 (ReadTheDocs 테마 사용)
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
