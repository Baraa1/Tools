const fileTempl = document.getElementById("file-template"),
imageTempl = document.getElementById("image-template"),
empty = document.getElementById("empty");
const messages = document.getElementById("messages");
//const messages = document.getElementById("messages");

// use to store pre selected files
//let FILES = {};

// check if file is of type image and prepend the initialied
// template to the target element
//function addFile(target, file) {
//    const isImage = file.type.match("image.*"),
//    objectURL = URL.createObjectURL(file);
//
//    const clone = isImage
//    ? imageTempl.content.cloneNode(true)
//    : fileTempl.content.cloneNode(true);
//
//    clone.querySelector("h1").textContent = file.name;
//    clone.querySelector("li").id = objectURL;
//    clone.querySelector(".delete").dataset.target = objectURL;
//    clone.querySelector(".size").textContent =
//    file.size > 1024
//        ? file.size > 1048576
//        ? Math.round(file.size / 1048576) + "mb"
//        : Math.round(file.size / 1024) + "kb"
//        : file.size + "b";
//
//    isImage &&
//    Object.assign(clone.querySelector("img"), {
//        src: objectURL,
//        alt: file.name
//    });
//
//    empty.classList.add("hidden");
//    target.prepend(clone);
//
//    FILES[objectURL] = file;
//}

//const gallery = document.getElementById("gallery"),
overlay = document.getElementById("overlay");

// click the hidden input of type file if the visible button is clicked
// and capture the selected files
const hidden   = document.getElementById("hidden-input");
const submit_btn = document.getElementById("submit")
const add_file = document.getElementById("button")
add_file.onclick = () => {
    hidden.click();
    if (empty !== null) {
        empty.classList.add("hidden")
    }
    //messages.classList.add("hidden")
}
//hidden.onchange = (e) => {
//    for (const file of e.target.files) {
//    addFile(gallery, file);
//    }
//};

// use to check if a file is being dragged
const hasFiles = ({ dataTransfer: { types = [] } }) =>
    types.indexOf("Files") > -1;

// use to drag dragenter and dragleave events.
// this is to know if the outermost parent is dragged over
// without issues due to drag events on its children
let counter = 0;

// reset counter and append file to gallery when file is dropped
function dropHandler(ev) {
    ev.preventDefault();
    for (const file of ev.dataTransfer.files) {
        //addFile(gallery, file);
        overlay.classList.remove("draggedover");
        //counter = 0;
        // Create a new File object
        let myFile = new File([file], file.name, {
            type: file.type,
            lastModified: file.lastModified,
        });

        // Now let's create a DataTransfer to get a FileList
        let dataTransfer = new DataTransfer();
        dataTransfer.items.add(myFile);
        //console.log(typeof hidden.files)
        hidden.files = dataTransfer.files;
    };
    add_file.style.pointerEvents = 'all';
    if (empty !== null) {
        empty.classList.add("hidden");
    }
    //messages.classList.add("hidden")
    submit_btn.click();
}

// only react to actual files being dragged
function dragEnterHandler(e) {
    e.preventDefault();
    if (!hasFiles(e)) {
        return;
    }
    //++counter && overlay.classList.add("draggedover");
    add_file.style.pointerEvents = 'none';
    overlay.classList.add("draggedover");
}

function dragLeaveHandler(e) {
    //1 > --counter && overlay.classList.remove("draggedover");
    overlay.classList.remove("draggedover");
    add_file.style.pointerEvents = 'all';
}

function dragOverHandler(e) {
    if (hasFiles(e)) {
        e.preventDefault();
    }
}

function hideModal() { 
    document.getElementById("defaultModal").style.display = 'none' 
};

// event delegation to caputre delete events
// fron the waste buckets in the file preview cards
//gallery.onclick = ({ target }) => {
//if (target.classList.contains("delete")) {
//  const ou = target.dataset.target;
//  document.getElementById(ou).remove(ou);
//  gallery.children.length === 1 && empty.classList.remove("hidden");
//  delete FILES[ou];
//}
//};

// print all selected files
//document.getElementById("submit").onclick = () => {
//    alert(`Submitted Files:\n${JSON.stringify(FILES)}`);
//    console.log(FILES);
//};

// clear entire selection
//document.getElementById("cancel").onclick = () => {
//    while (gallery.children.length > 0) {
//        gallery.lastChild.remove();
//    }
//    FILES = {};
//    empty.classList.remove("hidden");
//    gallery.append(empty);
//};

const sortableList = document.getElementById('gallery');
const itemOrderForm = document.getElementById('item-order-form');
const itemOrderInput = document.getElementById('item-order-input');
let items;
// Function to update data-item-id attributes based on current order
function updateItemIds() {
  const sortableItems = sortableList.querySelectorAll('.sortable-item');
  sortableItems.forEach((item, index) => {
    item.dataset.itemId = index + 1; // You can adjust the starting number if needed
  });
}

function validatePageRange(itemElement, pageRangeInput) {
  const pages = parseInt(itemElement.querySelector("#pages").textContent)
  console.log("2")
  // Validate the input: "number-number" or "number"
  const pattern = /^\d+(-\d+)?$/;
  let startPage
  let endPage;
  let newMessage;
  if (pattern.test(pageRangeInput)) {
    // Input is valid, extract the start and end page numbers
    //console.log(`Start Page: ${startPage}, End Page: ${endPage}`);
    // Now you can use the start and end page numbers as needed
    const pageRangeArray = pageRangeInput.split('-');
    if (pageRangeArray.length === 2) {
        // If there are two parts (start and end page), assign them to startPage and endPage
        [startPage, endPage] = pageRangeArray;
        startPage = parseInt(startPage)
        endPage   = parseInt(endPage)
    } else if (pageRangeArray.length === 1) {
        // If there's only one part, assign it to startPage
        startPage = pageRangeArray[0];
        endPage   = "False"
        startPage = parseInt(startPage)
    } else {
        // Input is not in the correct format
        newMessage = `<p class="text-center text-xl py-3 leading-relaxed text-white dark:text-red-400" style="background-color:rgb(220 38 38);">Please enter a valid page range in the format "1-20".</p>`
        messages.innerHTML = newMessage;
    }

    if (startPage > pages) {
        // Input is not in the correct format
        newMessage = `<p class="text-center text-xl py-3 leading-relaxed text-white dark:text-red-400" style="background-color:rgb(220 38 38);">Start page: ${startPage} Cannot be greater than the number of pages your file holds</p>`
        messages.innerHTML = newMessage;
    }
    else if (endPage > pages) {
        // Input is not in the correct format
        newMessage = `<p class="text-center text-xl py-3 leading-relaxed text-white dark:text-red-400" style="background-color:rgb(220 38 38);">End page: ${endPage} Cannot be greater than the number of pages your file holds</p>`
        messages.innerHTML = newMessage;
    }
    else if (startPage > endPage) {
        // Input is not in the correct format
        newMessage = `<p class="text-center text-xl py-3 leading-relaxed text-white dark:text-red-400" style="background-color:rgb(220 38 38);">End page: ${endPage} cannot be smaller than Start page: ${startPage}</p>`
        messages.innerHTML = newMessage;
    }
    else if (startPage <= 0 || endPage <= 0) {
        // Input is not in the correct format
        newMessage = `<p class="text-center text-xl py-3 leading-relaxed text-white dark:text-red-400" style="background-color:rgb(220 38 38);">Start page or End page cannot be less than 1</p>`
        messages.innerHTML = newMessage;
    }
    } else {
    // Input is not in the correct format
    newMessage = `<p class="text-center text-xl py-3 leading-relaxed text-white dark:text-red-400" style="background-color:rgb(220 38 38);">Please enter a valid page range in the format "1-20".</p>`
    messages.innerHTML = newMessage;
  }
  return [startPage, endPage]
}

function collectItemDetails() {
    const listitems = [];
    const itemElements = sortableList.querySelectorAll('.sortable-item');
  
    itemElements.forEach((itemElement) => {
      const itemId    = itemElement.dataset.itemId;
      const itemName  = itemElement.querySelector('input[name="item_name"]').value;
      const itemRange = itemElement.querySelector('input[name="page_range"]').value;
      let startPage   = "False";
      let endPage     = "False";
      if (itemRange !== "") {
        [startPage, endPage] = validatePageRange(itemElement ,itemRange)
      }

      listitems.push({
        id: itemId,
        name: itemName,
        startPage: startPage,
        endPage: endPage,
      });
    });
  
    return listitems;
}

/*itemOrderForm.addEventListener('change', (e) => {
    //e.preventDefault();
    // Serialize the item order array and set it as the value of the hidden input field
    const itemOrder = collectItemDetails();
    itemOrderInput.value = JSON.stringify(itemOrder);
    console.log('change');
    console.log(itemOrder);
    // Submit the form
    //itemOrderForm.submit();
});*/

function handleDragStart(e) {
    this.style.opacity = '0.4';
    dragSrcEl = this;

    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}
  
function handleDragEnd(e) {
    this.style.opacity = '1';
    items.forEach(function (item) {
        item.classList.remove('over');
    });
}

function handleDragOver(e) {
    e.preventDefault();
    return false;
}

/*function handleDragEnter(e) {
    this.classList.add('over');
}

function handleDragLeave(e) {
    this.classList.remove('over');
}*/

function orderList(){
    const itemOrder = collectItemDetails();
    itemOrderInput.value = JSON.stringify(itemOrder);
}

function handleDrop(e) {
    e.stopPropagation(); // stops the browser from redirecting.
    if (dragSrcEl !== this) {
        dragSrcEl.innerHTML = this.innerHTML;
        this.innerHTML = e.dataTransfer.getData('text/html');
        orderList();
    }
    return false;
}

function activateDrDo() {
    items = document.querySelectorAll('.sortable-item');
    items.forEach(function (item) {
        item.addEventListener('dragstart', handleDragStart);
        item.addEventListener('dragover', handleDragOver);
        //item.addEventListener('dragenter', handleDragEnter);
        //item.addEventListener('dragleave', handleDragLeave);
        item.addEventListener('dragend', handleDragEnd);
        item.addEventListener('drop', handleDrop);
    });
}

// Initialize item order when the page loads
updateItemIds();
activateDrDo();
orderList();

function removeLiParent(element) {
    let currentNode = element;
    while (currentNode !== null) {
      if (currentNode.tagName === 'LI') {
        currentNode.remove();
        return true; // Found an <li> parent
      }
      currentNode = currentNode.parentNode;
    }
    return false; // No <li> parent found
}