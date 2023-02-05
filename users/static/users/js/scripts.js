document.getElementById('nav').onmouseover = function(event) {
  let target = event.target;
  if (target.className == 'menu-item') {
    let s = target.getElementsByClassName('submenu');
    closeMenu();
    s[0].style.display='block';
  }
}

document.onmouseover=function (event) {
  let target = event.target;
  console.log(event.target);
  if (target.className!='menu-item' && target.className!='submenu') {
    closeMenu();
  }
}

function closeMenu() {
  let menu = document.getElementById('nav');
  let subm=document.getElementsByClassName('submenu')
  for (let i=0; i < subm.length; i++) {
    subm[i].style.display="none";
  }
}






// function myFunction() {
//     document.getElementById("myDropdown").classList.toggle("show");
// }
//
// // Close the dropdown menu if the user clicks outside of it
// window.onclick = function(event) {
//   if (!event.target.matches('.dropbtn')) {
//
//     let dropdowns = document.getElementsByClassName("dropdown-content");
//     let i;
//     for (i = 0; i < dropdowns.length; i++) {
//       let openDropdown = dropdowns[i];
//       if (openDropdown.classList.contains('show')) {
//         openDropdown.classList.remove('show');
//       }
//     }
//   }
// }
