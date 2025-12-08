const span = document.getElementById('pas-display')
const span2 = document.getElementById('display-pas')

const img = document.getElementById('toggle-img')
const img2 = document.getElementById('img-toggle')

const passwordInput = document.getElementById('pas-input')
const passwordInput2 = document.getElementById('input-pas')


const togglePassword = (el, image, input) => {

  el.addEventListener('click', () => {

    if (input.type === 'password') {
      input.type = 'text'
      image.src = '/static/icons/hide-password.png'
      image.alt = 'hide password'
    } else {
      input.type = 'password'
      image.src = '/static/icons/show_password.png'
      image.alt = 'show password'
    }

  })
}

togglePassword(span, img, passwordInput);
togglePassword(span2, img2, passwordInput2);


// Check Password match
const register = document.getElementById('custom-register-btn')
const errorP = document.getElementById('reg-err-msg')
let errorMsg = errorP.innerText

register.onclick = (e) => {
  e.preventDefault()
  let password = passwordInput.value
  let repeatedPassword = passwordInput2.value
  
  console.log(`Password: ${password}, Repeated: ${repeatedPassword}`)

  if (password !== repeatedPassword) {
    errorMsg = "Passwords do not match"
    return;
  }

  register.closest('form').submit();

}