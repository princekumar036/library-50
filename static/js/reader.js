let toc_data = document.querySelector('.inserted-toc')
let toc_btn = document.querySelector('.nav-toc')

toc_btn.addEventListener('click', () => {
    toc_data.classList.toggle('hidden')
})