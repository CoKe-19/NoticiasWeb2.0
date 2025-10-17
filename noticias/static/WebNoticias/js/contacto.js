document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');

    if(!contactForm) return;
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    contactForm.addEventListener('submit', async e => {
        e.preventDefault();
        const formData = new FormData(contactForm);

        const response = await fetch("/contacto/ajax/", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData,
        });

        const data = await response.json();

        if(data.success){
            formMessage.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            contactForm.reset();
        } else {
            if(data.errors){
                let errorHTML = '<div class="alert alert-danger"><ul>';
                for(const field in data.errors){
                    errorHTML += `<li>${field}: ${data.errors[field]}</li>`;
                }
                errorHTML += '</ul></div>';
                formMessage.innerHTML = errorHTML;
            } else {
                formMessage.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
            }
        }
    });
});
