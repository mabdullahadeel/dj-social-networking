console.log("Hello From Profile Page JS")

document.getElementById('nav-profile').addEventListener('click', () => {
    console.log('Event Listner activated')
    let element = document.getElementById('editProfile');
    element.classList.add('active')
    element.classList.add('show')
    // removing class from other
    document.getElementById('work').classList.remove('active')
    document.getElementById('studio').classList.remove('active')
    document.getElementById('favorite').classList.remove('active')
})