function dark()
{
  console.log("testse");
  let icons = document.querySelectorAll('button.icon');
  icons.forEach(icon =>{
    if(icon.id != "head-btn" && icon.id != "head-span")
    {
        icon.classList.toggle('button-dark-mode');
    }
    
  });
  /*
  let navlink = document.querySelectorAll('.nav-link');
  navlink.forEach(navlk =>{
    navlk.classList.toggle('whiteFontColor');
  });
  const navbarbrand = document.querySelector(".navbar-brand");
  navbarbrand.classList.toggle("whiteFontColor");*/
  const separation_border = document.querySelector(".separation_border");
  if(separation_border)
  {
    document.querySelector(".separation_border").classList.toggle('separation_border-dark-mode');
  }
  //document.querySelector(".navbar-toggler").classList.toggle('toggler-icon-dark');
  /*document.querySelectorAll('.btn').forEach(btn =>{
    btn.classList.toggle('button-dark-mode');
  });*/
  document.querySelectorAll('.card-body').forEach(card =>{
    card.classList.toggle('dark-mode-body');
  });
  document.querySelectorAll('.title').forEach(title =>{
    title.classList.toggle('dark-nav');
  });
  document.querySelectorAll('.nav-item').forEach(item =>{
    item.classList.toggle('dark-nav');
  });
  document.querySelectorAll('.form-control').forEach(form_control =>{
    form_control.classList.toggle('textarea-dark');;
  });

  document.querySelectorAll('.page-link').forEach(btn =>{
    	btn.classList.toggle('page-link-dark-mode');
  });
  document.querySelector('body').classList.toggle('dark-mode-body');
  document.querySelector('nav').classList.toggle('dark-mode-nav');
  document.getElementById('footer').classList.toggle('dark-mode-body');
  let recipefull = document.querySelector('.recipe-info');
  if(localStorage.getItem("mode")=="dark")
  {
    localStorage.setItem("mode", "light");
    if(recipefull)
    {
      darkfull();
    }
  }
  else
  {
    localStorage.setItem("mode", "dark");
    if(recipefull)
    {
      darkfull();
    }
  }
}

let darkmode = document.getElementById("Dark-mode");
if(darkmode)
{
    
    darkmode.addEventListener('click',dark);

    if(localStorage.getItem("mode")=="dark")
    {
    localStorage.setItem("mode", "light");
    dark();
    }
}