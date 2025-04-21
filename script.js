document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('verificationForm');
    const screenshotInput = document.getElementById('screenshot');
    const screenshotPreview = document.getElementById('screenshotPreview');
    const submitButton = form.querySelector('button[type="submit"]');

    // Handle image preview
    screenshotInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                screenshotPreview.innerHTML = '';
                screenshotPreview.appendChild(img);
            }
            reader.readAsDataURL(file);
        }
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const screenshot = screenshotInput.files[0];

        if (!name || !screenshot) {
            alert('请填写姓名并上传截图！');
            return;
        }

        // Disable submit button and show loading state
        submitButton.disabled = true;
        submitButton.textContent = '正在验证...';

        try {
            const formData = new FormData();
            formData.append('name', name);
            formData.append('screenshot', screenshot);

            const response = await fetch('/verify', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                alert(result.message);
                form.reset();
                screenshotPreview.innerHTML = '';
            } else {
                alert(result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('提交失败，请稍后重试');
        } finally {
            // Re-enable submit button
            submitButton.disabled = false;
            submitButton.textContent = '提交验证';
        }
    });
});
