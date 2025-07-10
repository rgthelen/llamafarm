#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🌾 LLaMA Farm Publishing Script${NC}"
echo ""

# Check if logged in to npm
echo -e "${YELLOW}Checking npm login...${NC}"
npm_user=$(npm whoami 2>/dev/null)
if [ -z "$npm_user" ]; then
    echo -e "${RED}❌ Not logged in to npm. Please run 'npm login' first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Logged in as: $npm_user${NC}"

# Clean and build
echo -e "${YELLOW}Cleaning and building...${NC}"
rm -rf dist/
npm run build
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Build successful${NC}"

# Run tests (when available)
# echo -e "${YELLOW}Running tests...${NC}"
# npm test
# if [ $? -ne 0 ]; then
#     echo -e "${RED}❌ Tests failed${NC}"
#     exit 1
# fi
# echo -e "${GREEN}✅ Tests passed${NC}"

# Get current version
current_version=$(node -p "require('./package.json').version")
echo ""
echo -e "${YELLOW}Current version: $current_version${NC}"
echo "Version bump options:"
echo "  1) Patch (x.x.X)"
echo "  2) Minor (x.X.0)"
echo "  3) Major (X.0.0)"
echo "  4) Keep current version"
read -p "Choose option (1-4): " version_choice

case $version_choice in
    1)
        npm version patch
        ;;
    2)
        npm version minor
        ;;
    3)
        npm version major
        ;;
    4)
        echo "Keeping current version"
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

# Get new version
new_version=$(node -p "require('./package.json').version")
echo -e "${GREEN}Publishing version: $new_version${NC}"

# Dry run first
echo ""
echo -e "${YELLOW}Running dry-run...${NC}"
npm publish --dry-run --access public

echo ""
read -p "Proceed with actual publish? (y/N): " confirm
if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
    echo -e "${YELLOW}Publishing to npm...${NC}"
    npm publish --access public
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Successfully published @llamafarm/llamafarm@$new_version${NC}"
        echo ""
        echo "Users can now install with:"
        echo -e "${GREEN}npm install -g @llamafarm/llamafarm${NC}"
    else
        echo -e "${RED}❌ Publishing failed${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Publishing cancelled${NC}"
fi 