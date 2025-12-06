const filterBar = document.getElementById('filterBar');

filterBar.addEventListener('click', (e) => {
  if (e.target.tagName !== 'INPUT' && e.target.tagName !== 'BUTTON') {
    filterBar.classList.toggle('expanded');
  }
});


// Tables per section
const sectionText = document.getElementById('section')

const allIcon = document.getElementById('all-icon')
const allBooks = document.getElementById('books')

const locatorIcon = document.getElementById('locator')
const bookLocation = document.getElementById('location')

const borrowedIcon = document.getElementById('borrowed-icon')
const borrowed = document.getElementById('borrowed')

const damagedIcon = document.getElementById('damaged-icon')
const damaged = document.getElementById('damaged')

// checkout
const checkOutIcon = document.getElementById('co-icon')
const checkout = document.getElementById('checkout')


locatorIcon.onclick = () => {
  allBooks.style.display = 'none'
  borrowed.style.display = 'none'
  damaged.style.display = 'none'
  bookLocation.style.display = 'block'
  sectionText.innerText = 'Book Location'
}
borrowedIcon.onclick = () => {
  allBooks.style.display = 'none'
  bookLocation.style.display = 'none'
  damaged.style.display = 'none'
  borrowed.style.display = 'block'
  sectionText.innerText = 'Borrowed Books'
}
damagedIcon.onclick = () => {
  allBooks.style.display = 'none'
  borrowed.style.display = 'none'
  bookLocation.style.display = 'none'
  damaged.style.display = 'block'
  sectionText.innerText = 'Damaged Books'
}
allIcon.onclick = () => {
  borrowed.style.display = 'none'
  damaged.style.display = 'none'
  bookLocation.style.display = 'none'
  allBooks.style.display = 'block'
  sectionText.innerText = 'All Books'
}

// checkOutIcon.onclick = () => {
//   borrowed.style.display = 'none'
//   damaged.style.display = 'none'
//   bookLocation.style.display = 'none'
//   allBooks.style.display = 'none'
//   filterBar.style.display = 'none'
//   checkout.style.display = 'block'
//   sectionText.innerText = 'Checkout'
// }