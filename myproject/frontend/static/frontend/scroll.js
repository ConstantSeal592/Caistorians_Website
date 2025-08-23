console.log("Loaded")

magazines = document.getElementById("magazines");
left = document.getElementById("scroll_left");
right = document.getElementById("scroll_right");

left.addEventListener('click', () => {
    //magazines.scrollBy({Left: 320, behavour: 'smooth'})
    magazines.scrollLeft -= 350 * 2;
})
right.addEventListener('click', () => {
    console.log("clcik")
    //magazines.scrollBy({Left: -320, behavour: 'smooth'})
    magazines.scrollLeft += 350 * 2;
})