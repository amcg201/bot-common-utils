#!/bin/bash

cd "/Users/aaronmcgilligan/Documents/Trading Bots/Common_files" || exit

echo "📄 Current Git status:"
git status
echo ""

read -p "✅ Proceed with committing and pushing all changes? (y/n): " confirm

if [[ $confirm == "y" || $confirm == "Y" ]]; then
    git add .

    echo "Enter your Git commit message:"
    read commit_message

    git commit -m "$commit_message"
    git push

    echo "✅ GitHub updated successfully!"
else
    echo "❌ Git push cancelled."
fi

