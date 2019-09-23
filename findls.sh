find . \
  -not -path './.git' \
  -not -path './.git/*' \
  -not -path '*.cabal' \
  -not -path '*.json' \
  -not -path '*.md' \
  -not -path '*.docx' \
  -type f
