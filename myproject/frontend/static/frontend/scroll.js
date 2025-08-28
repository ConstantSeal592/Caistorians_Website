magazines = document.getElementById("magazines");
magleft = document.getElementById("scroll_left_mag");
magright = document.getElementById("scroll_right_mag");

magleft.addEventListener('click', () => {
    //magazines.scrollBy({Left: 320, behavour: 'smooth'})
    magazines.scrollLeft -= 350 * 2;
})
magright.addEventListener('click', () => {
    console.log("clcik")
    //magazines.scrollBy({Left: -320, behavour: 'smooth'})
    magazines.scrollLeft += 350 * 2;
})




members = document.getElementById("membersScroll")
memleft = document.getElementById("scroll_left_mem")
memright = document.getElementById("scroll_right_mem")

memleft.addEventListener('click', () => {
    members.scrollLeft -= 500;
})
memright.addEventListener('click', () => {
    console.log('click')
    members.scrollLeft += 500;
})