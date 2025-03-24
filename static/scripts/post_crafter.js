// Post Crafter JavaScript
console.log("post_crafter.js loaded");

$(document).ready(function() {
    console.log("Post crafter document ready");

    // Only run if we're on the post crafter page
    if (!$('#postCrafterForm').length) {
        console.log("No post crafter form found on this page");
        return;
    }

    console.log("Initializing post crafter functionality");

    // Character counters
    const $titleInput = $('#postTitle');
    const $titleCounter = $('#titleCounter');
    const $contentInput = $('#postContent');
    const $contentCounter = $('#contentCounter');

    $titleInput.on('input', function() {
        console.log("Title input changed:", $(this).val().length);
        $titleCounter.text($(this).val().length);
    });

    $contentInput.on('input', function() {
        $contentCounter.text($(this).val().length);
    });

    // Tag previewer
    const $tagsInput = $('#postTags');
    const $tagPreview = $('#tagPreview');

    $tagsInput.on('input', function() {
        const tags = $(this).val().split(',').filter(tag => tag.trim() !== '');
        $tagPreview.empty();

        tags.slice(0, 5).forEach(tag => {
            $('<span>')
                .addClass('badge bg-primary me-2 mb-2')
                .text(tag.trim())
                .appendTo($tagPreview);
        });
    });

    // Preview toggle
    const $previewToggle = $('#previewToggle');
    const $previewArea = $('#previewArea');
    const $previewTitle = $('#previewTitle');
    const $previewTags = $('#previewTags');
    const $previewContent = $('#previewContent');

    $previewToggle.on('click', function() {
        console.log("Preview toggle clicked");
        // Toggle preview visibility
        if ($previewArea.hasClass('d-none')) {
            $previewArea.removeClass('d-none');
            $(this).html('<i class="fas fa-edit me-2"></i>Continue Editing');

            // Update preview content
            $previewTitle.text($titleInput.val() || 'Post Title');

            // Update tags
            $previewTags.empty();
            const tags = $tagsInput.val().split(',').filter(tag => tag.trim() !== '');
            tags.slice(0, 5).forEach(tag => {
                $('<span>')
                    .addClass('badge bg-secondary me-2')
                    .text(tag.trim())
                    .appendTo($previewTags);
            });

            // Format content (basic markdown-like parsing)
            let formattedContent = $contentInput.val()
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
                .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
                .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
                .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" class="img-fluid rounded my-2">')
                .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank">$1</a>');

            $previewContent.html(formattedContent || 'Post content will appear here...');
        } else {
            $previewArea.addClass('d-none');
            $(this).html('<i class="fas fa-eye me-2"></i>Preview Post');
        }
    });

    // Format buttons
    $('.format-btn').on('click', function() {
        console.log("Format button clicked:", $(this).data('format'));

        const format = $(this).data('format');
        const $textarea = $('#postContent');
        const textarea = $textarea[0];
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const selectedText = $textarea.val().substring(start, end);

        let formattedText = '';

        switch (format) {
            case 'bold':
                formattedText = `**${selectedText}**`;
                break;
            case 'italic':
                formattedText = `*${selectedText}*`;
                break;
            case 'heading':
                formattedText = `## ${selectedText}`;
                break;
            case 'list':
                formattedText = selectedText.split('\n').map(line => `- ${line}`).join('\n');
                break;
            case 'link':
                const url = prompt('Enter URL:', 'https://');
                if (url) {
                    formattedText = `[${selectedText || 'Link text'}](${url})`;
                } else {
                    return;
                }
                break;
            case 'image':
                const imageUrl = prompt('Enter image URL:', 'https://');
                if (imageUrl) {
                    formattedText = `![${selectedText || 'Image description'}](${imageUrl})`;
                } else {
                    return;
                }
                break;
            case 'code':
                formattedText = '```\n' + selectedText + '\n```';
                break;
        }

        // Insert the formatted text
        $textarea.focus();
        const currentValue = $textarea.val();
        const newValue = currentValue.substring(0, start) + formattedText + currentValue.substring(end);
        $textarea.val(newValue);

        // Update character count
        $contentCounter.text($textarea.val().length);

        // Set cursor position after the inserted text
        const newPosition = start + formattedText.length;
        textarea.setSelectionRange(newPosition, newPosition);
    });

    // Form submission
    const $form = $('#postCrafterForm');
    const $draftBtn = $('#draftBtn');
    const $publishBtn = $('#publishBtn');
    const $saveAsDraft = $('#saveAsDraft');

    $form.on('submit', function(e) {
        console.log("Form submitted");
        // Set action based on which button was clicked
        if (e.originalEvent && e.originalEvent.submitter === $draftBtn[0] || $saveAsDraft.prop('checked')) {
            console.log("Saving as draft");
            $(this).attr('action', '/community/save_draft');
        } else {
            console.log("Publishing post");
            $(this).attr('action', '/community/create_post');
        }
    });

    // Call some functions to initialize the UI
    // Set initial character counts
    $titleCounter.text($titleInput.val().length);
    $contentCounter.text($contentInput.val().length);

    // Trigger tag preview on initial load if there are any tags
    if ($tagsInput.val().trim()) {
        $tagsInput.trigger('input');
    }

    console.log("Post crafter initialization complete");
});
