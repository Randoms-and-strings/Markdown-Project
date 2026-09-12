// let submitFile = document.querySelector("form");
// let deleteBlock = document.querySelector(".delete-label"); //code needs update
// let inputFieldExpand = document.querySelector("input");
// let newElementOptions = document.querySelectorAll(".add-element");
// let newElementSelectContainer = document.querySelector(".pick-new-element");
// let placeholderPreviewImageVar;
// // console.log(newElementSelectContainer)

// // TOGGLE OPTION TO SHOW/HIDE CREATE NEW ELEMENT OPTIONS
// document.querySelector(".add-label").addEventListener("click", (event) => {
//     let optionsBox = document.querySelector("#options");
//     if(optionsBox.classList.contains("hide-element")){
//         optionsBox.classList.remove("hide-element");
//     }else{
//         optionsBox.classList.add("hide-element");
//     }
// });

// // SUBMIT BUTTON NOT IN FORM TAG, SO EVENT LISTENER MAKES IT SUBMIT THE FORM
// // IF CERTAIN CONDITIONS ARE MET
// // 1) IF THE USER IS NOT JUST TRYING TO SUBMIT THE TITLE ALONE
// // 2) IF THERE'S A LIST CONTAINER; SAVES THE TOTAL VALUE IN AN HIDDEN INPUT FIELD.
// //      STRUCTURE IS LISTDIV > INPUT,UL>contentEditable LI
// document.querySelector(".submit-note").addEventListener("click", (event) => {
//     let ulExists = document.querySelectorAll(".ul-div");
//     let globalContainerCount =document.querySelectorAll("form > div");
//     let toAddNameInputs = document.querySelector("form").children;
//     let articleOrder = 1;
    
//     // console.log(toAddNameInputs);

//     if(globalContainerCount.length <= 2){
//         event.preventDefault();
//         alert("you need to write a proper article to submit!");
//         return
//     }

//     if(ulExists.length > 0){
        
//         for(let i=0; i < ulExists.length; i++){
//             let respectiveListInputs = null;
//             let listDivChildren = ulExists[i].children;
//             let allUlChildren = null;

//             for(let j=0; j<listDivChildren.length;j++){
//                 // console.log(listDivChildren[j].tagName);
//                 if(listDivChildren[j].tagName === "INPUT"){
//                     respectiveListInputs = listDivChildren[j];
//                     respectiveListInputs.value = "";   //this clears the value incase of network issue and reloads
//                 }else if(listDivChildren[j].tagName === "UL"){
//                     allUlChildren = listDivChildren[j].children;
//                 }
//             }

//             for(let j = 0; j<allUlChildren.length;j++){
//                 respectiveListInputs.value += allUlChildren[j].innerText + "/<newlinechar>";
// //                    respectiveListInputs.value = "hello";
//             }
// //             console.log(respectiveListInputs.value);
            
//         }
//     }

//     console.log(toAddNameInputs);
//     for(let i = 1; i < toAddNameInputs.length - 1; i++){

//         let forInput = toAddNameInputs[i].querySelector("input");
//         if(forInput){
            
//             if(forInput.value.trim().length < 1){
//                 continue;
//             }
//             articleOrder += 1;
//             forInput.name = `${forInput.dataset.type}:${articleOrder}`;
//             // console.log(forInput);
//             continue;
//         }
        

//         let forTextArea = toAddNameInputs[i].querySelector("textarea");
        
//         if(forTextArea.value.trim().length < 1){
//                 continue;
//         }
//         articleOrder += 1;
//         forTextArea.name = `${forTextArea.dataset.type}:${articleOrder}`;
//         // console.log(forTextArea);
//     }

//     console.log(articleOrder);
//     submitFile.submit();
// });

// // EVENT LISTENER FOR DELETE BUTTON TO WIPE A DIV(INPUT/TEXTAREA) FIELD;
// deleteBlock.addEventListener("click", deleteElementContainer);

// // IF AN INPUT GETS TOO LONG, IT GETS CHANGED TO TEXT AREA
// // THE NEW TEXTAREA DELETES EXCESS ROWS WITH DEL/BACKSPACE;
// inputFieldExpand.addEventListener("focusout", removeBorder);
// inputFieldExpand.addEventListener("input", expandInputField);

// // EVENT LISTENER FOR BUTTON THAT ADDS NEW ELEMENT
// for(let i = 0; i< newElementOptions.length; i++){
//     // console.log(newElementOptions[i]);
//     switch(newElementOptions[i].id){
//         case "img":
//             newElementOptions[i].addEventListener("click", (event) => {

//             // https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentElement

//             let newImgUploadDiv = document.createElement("div");
//             let newImgInput = document.createElement("input");
//             let newImgPreview = document.createElement("img");
//             let pseudoDeleteImg = document.createElement("i");
//             // newImgInput.style.backgroundColor = "red";

//             newImgUploadDiv.classList.add("image-div");

//             let deleteImg = addClassesToElement(deleteBlock, pseudoDeleteImg);
//             deleteImg.classList.remove("delete-label");
//             deleteImg.classList.add("img-delete-label");
//             deleteImg.style.color = "white";
//             deleteImg.style.backgroundColor = "black";

//             newImgUploadDiv.style.height = "400px";
//             newImgUploadDiv.appendChild(newImgInput);
//             newImgUploadDiv.appendChild(newImgPreview);

//             newImgInput.type = "file";
//             newImgInput.accept = "image/*";
//             newImgInput.setAttribute("data-type", "img");

//             newImgPreview.style.display = "none";
//             newImgPreview.alt = "image preview";
           
//             newImgInput.addEventListener("change", (event) => {
//                 previewImageUpload(newImgPreview, event.target, newImgUploadDiv);
//             });
//             deleteImg.addEventListener("click", deleteElementContainer);
//             newImgUploadDiv.appendChild(deleteImg);
//             // newImgUploadDiv.appendChild(newImgPreview);
//             newElementSelectContainer.insertAdjacentElement("beforebegin", newImgUploadDiv);
//             });
//             break;

//         case "h2":
//             newElementOptions[i].addEventListener("click", (event) => {
//                let newHeadingUploadDiv = document.createElement("div");
//                let newH2 =  document.createElement("input");
//                let pseudoDeleteLabel = document.createElement("i");

//                newHeadingUploadDiv.classList.add("h2-div");
//                newH2.classList.add("new-h2-elements-input");
//                newH2.setAttribute("data-type", "h2");
//                let deleteLabel = addClassesToElement(deleteBlock, pseudoDeleteLabel);

//                newH2.addEventListener("focusout", removeBorder);
//                newH2.addEventListener("input", expandInputField);
//                deleteLabel.addEventListener("click", deleteElementContainer);

//                newHeadingUploadDiv.appendChild(newH2);
//                newHeadingUploadDiv.appendChild(deleteLabel);
               
//                newElementSelectContainer.insertAdjacentElement("beforebegin", newHeadingUploadDiv);
//             });
//             break;
        
//         case "p":
            
//             newElementOptions[i].addEventListener("click", (event) => {
//                let newParagraphUploadDiv = document.createElement("div");
//                let newP =  document.createElement("input");
//                let pseudoDeleteLabel = document.createElement("i");

//                newParagraphUploadDiv.classList.add("p-div");
//                newP.classList.add("new-p-elements-input");
//                newP.setAttribute("data-type", "p");
//                let deleteLabel = addClassesToElement(deleteBlock, pseudoDeleteLabel);

//                newP.addEventListener("input", expandInputField);
//                newP.addEventListener("focusout", removeBorder);
//                deleteLabel.addEventListener("click", deleteElementContainer);

//                newParagraphUploadDiv.appendChild(newP);
//                newParagraphUploadDiv.appendChild(deleteLabel);
               
//                newElementSelectContainer.insertAdjacentElement("beforebegin", newParagraphUploadDiv);
//             });
//             break;

//         case "ul":
            
//             newElementOptions[i].addEventListener("click", (event) => {
//                 let listDiv = document.createElement("div");
//                 let ulistItem = document.createElement("ul");

//                 let listItem = document.createElement("li");
//                 let pseudoDeleteLabel = document.createElement("i");
//                 let deleteLabel = addClassesToElement(deleteBlock, pseudoDeleteLabel);
//                 let savingToInput = document.createElement("input");

//                 // make list content editable && append to div
//                 listItem.contentEditable = "true";
//                 listItem.classList.add("remove-borders");

//                 savingToInput.style.display = "none";
//                 // savingToInput.name = "list";
//                 savingToInput.setAttribute("data-type", "ul");

//                 listItem.focus();
//                 listDiv.classList.add("ul-div")
//                 listDiv.appendChild(savingToInput);
//                 listDiv.appendChild(ulistItem);
//                 listDiv.appendChild(deleteLabel);

//                 ulistItem.appendChild(listItem);

//                 deleteLabel.addEventListener("click", deleteElementContainer);

//                 listItem.addEventListener("keydown", (event) => {
//                     // 
//                     createListItems(event, ulistItem, savingToInput);
//                     // console.log(savingToInput.value);
//                 });
//                 // listItem.addEventListener("onfocusout")
                
//                 newElementSelectContainer.insertAdjacentElement("beforebegin", listDiv);
//             });
//             break;
//     }
// }

// // ----------------------------------------------------------------------------------------------------------------------------------
// // ///ALL FUNCTIONS BELOW

// function createListItems(event, ulContainer, hiddenInput){
   
//     if(event.key === "Enter"){
//         event.preventDefault();
//         let newListItem = document.createElement("li");
//         newListItem.contentEditable = "true";
//         newListItem.classList.add("remove-borders");
//         ulContainer.appendChild(newListItem);
//         console.log(newListItem.innerText.length);
//         newListItem.innerText.trim();
//         newListItem.addEventListener("keydown", (event) => {
//             createListItems(event, ulContainer, hiddenInput);
//             // console.log(hiddenInput.value);
//         });
//         newListItem.focus()
//         // hiddenInput.value += event.target.innerText + "\n";

//     }else if(event.key === "Backspace" || event.key === "Delete"){
//         console.log(event.target.innerText.length);
        
//         if(event.target.innerText.length <= 1){

//             if(event.target.parentElement.childElementCount < 2){
//                 event.target.parentElement.parentElement.remove();
//                 return;
//             }
//             event.target.remove();
//         }
//     }
// }

// function addClassesToElement(fromElement, toElement){
//     for(let i = 0; i < fromElement.classList.length; i++){
//         toElement.classList.add(fromElement.classList[i]);
//     }
//     return toElement;
// }

// function removeBorder(event){
// //console.log("border remove")
//         if(event.target.value.trim().length > 0){
//             // console.log("condition");
//             event.target.classList.add("remove-borders");
//         }else{
//             if(event.target.classList.contains("remove-borders")){
//                 event.target.classList.remove("remove-borders"); 
//             }
//         }
// }

// function createTextArea(externalEvent){
//     let inputAttributes = externalEvent.target.attributes;
//             // console.log(inputFieldExpand[i].value);
//     let textArea = document.createElement("textarea");

//     for (const attr of inputAttributes) {
//         textArea.setAttribute(attr.name, attr.value);
//         // console.log(textArea);
//     }
    
//     textArea.setAttribute("rows", "2");
//     textArea.value = externalEvent.target.value;
//     textArea.setAttribute("value", externalEvent.target.value);
//     return textArea;
// }

// function expandInputField(event){
//     if(event.target.scrollWidth > event.target.clientWidth){// CHECK IT SCROLL WIDTH HIGHER THAN CLIENT SCREEN ELEMENT WIDTH TO CHANGE TO TEXTAREA;
//         let newTextArea = createTextArea(event);

//         newTextArea.addEventListener("input", increaseTextAreaHeight);
//         newTextArea.addEventListener("keydown", backspaceDeleteRowsTextArea);
//         newTextArea.addEventListener("focusout", removeBorder);
//         event.target.replaceWith(newTextArea);
//         newTextArea.focus();
//         const rect = newTextArea.getBoundingClientRect();
//         simulated_event = {
//             target: newTextArea,
//         };
//         increaseTextAreaHeight(simulated_event);
//     }
// }

// function increaseTextAreaHeight(event){
// //    console.log(event.target.scrollHeight, event.target.clientHeight);
//     if(event.target.scrollHeight > event.target.clientHeight){
//         // my original solution
//         let rowSize = parseInt(event.target.getAttribute("rows")) + 1;
//         // console.log(textArea.getAttribute("rows"), rowSize);
//         event.target.rows = `${rowSize}`;
//         event.target.setAttribute("rows", `${rowSize}`);
//         increaseTextAreaHeight(event);
// //           dont really know why this works, but it works....
// //            event.target.dispatchEvent(new Event('input', { 'bubbles': true }))

// //        online solution
// //        event.target.style.height = '0';
// //
// //        event.target.style.height = (textarea.scrollHeight + 16) + 'px'

//     }
// }

// function backspaceDeleteRowsTextArea(event){
//     if(event.key === "Backspace" || event.key === "Delete"){
//         const rect = event.target.getBoundingClientRect();
//         if(event.target.value[event.target.value.length - 1] == "\n" ){
//             let currentTextRows = event.target.rows;
//             let newTextRows = parseInt(currentTextRows) - 1;
//             event.target.setAttribute("rows", `${newTextRows}`);
//             // if(event.target.clientHeight > event.target.scrollHeight){
//             //     console.log("called:", event.target.clientHeight, event.target.scrollHeight);
//             //     backspaceDeleteRowsTextArea(event);
//             // }
//         }else if(event.target.value.trim().length < 1){
//             deleteElementContainer(event);
//         }
//     }
// }

// function previewImageUpload(previewElement, inputElement, container){
//     // my solution based on MDN Docs..
//     // console.log(this.files, this.files[0].size); for the input element
//     console.log(previewElement);
//     previewElement.style.display = "block";
//     previewElement.src = URL.createObjectURL(inputElement.files[0]);
//     container.style.height = "auto";
// }

// function deleteElementContainer(event){
//     console.log(event);
//         // console.log(deleteBlock[i].parentElement.children[0]);
//     if(event.target.parentElement.querySelector('.title-input')){
//         alert("can't have an article without a title man🙄🙄")
//         return;
//     }
//     event.target.parentElement.remove();
// }
let submitFile = document.querySelector("form");
let deleteBlock = document.querySelector(".delete-label"); //code needs update
let inputFieldExpand = document.querySelector("input");
let newElementOptions = document.querySelectorAll(".add-element");
let newElementSelectContainer = document.querySelector(".pick-new-element");
let h1Input = document.querySelector(".title-input");
let placeholderPreviewImageVar;
// console.log(newElementSelectContainer)

// TOGGLE OPTION TO SHOW/HIDE CREATE NEW ELEMENT OPTIONS
document.querySelector(".add-label").addEventListener("click", (event) => {
    let optionsBox = document.querySelector("#options");
    if(optionsBox.classList.contains("hide-element")){
        optionsBox.classList.remove("hide-element");
    }else{
        optionsBox.classList.add("hide-element");
    }
});

// SUBMIT BUTTON NOT IN FORM TAG, SO EVENT LISTENER MAKES IT SUBMIT THE FORM
// IF CERTAIN CONDITIONS ARE MET
// 1) IF THE USER IS NOT JUST TRYING TO SUBMIT THE TITLE ALONE
// 2) IF THERE'S A LIST CONTAINER; SAVES THE TOTAL VALUE IN AN HIDDEN INPUT FIELD.
//      STRUCTURE IS LISTDIV > INPUT,UL>contentEditable LI
document.querySelector(".submit-note").addEventListener("click", (event) => {
    let ulExists = document.querySelectorAll(".ul-div");
    let globalContainerCount =document.querySelectorAll("form > div");
    let toAddNameInputs = document.querySelector("form").children;
    let articleOrder = 1;
    
    // console.log(toAddNameInputs);

    if(globalContainerCount.length <= 2){
        event.preventDefault();
        alert("you need to write a proper article to submit!");
        return
    }

    if(ulExists.length > 0){
        
        for(let i=0; i < ulExists.length; i++){
            let respectiveListInputs = null;
            let listDivChildren = ulExists[i].children;
            let allUlChildren = null;

            for(let j=0; j<listDivChildren.length;j++){
                // console.log(listDivChildren[j].tagName);
                if(listDivChildren[j].tagName === "INPUT"){
                    respectiveListInputs = listDivChildren[j];
                    respectiveListInputs.value = "";   //this clears the value incase of network issue and reloads
                }else if(listDivChildren[j].tagName === "UL"){
                    allUlChildren = listDivChildren[j].children;
                }
            }

            for(let j = 0; j<allUlChildren.length;j++){
                respectiveListInputs.value += allUlChildren[j].innerText + "/<newlinechar>";
//                    respectiveListInputs.value = "hello";
            }
//             console.log(respectiveListInputs.value);
            
        }
    }

    console.log(toAddNameInputs);
    for(let i = 1; i < toAddNameInputs.length - 1; i++){

        let forInput = toAddNameInputs[i].querySelector("input");
        if(forInput){
            
            if(forInput.value.trim().length < 1){
                continue;
            }
            articleOrder += 1;
            forInput.name = `${forInput.dataset.type}:${articleOrder}`;
            // console.log(forInput);
            continue;
        }
        

        let forTextArea = toAddNameInputs[i].querySelector("textarea");
        
        if(forTextArea.value.trim().length < 1){
                continue;
        }
        articleOrder += 1;
        forTextArea.name = `${forTextArea.dataset.type}:${articleOrder}`;
        // console.log(forTextArea);
    }

    console.log(articleOrder);
    submitFile.submit();
});

// EVENT LISTENER FOR DELETE BUTTON TO WIPE A DIV(INPUT/TEXTAREA) FIELD;
deleteBlock.addEventListener("click", deleteElementContainer);

// IF AN INPUT GETS TOO LONG, IT GETS CHANGED TO TEXT AREA
// THE NEW TEXTAREA DELETES EXCESS ROWS WITH DEL/BACKSPACE;
inputFieldExpand.addEventListener("focusout", removeBorder);
inputFieldExpand.addEventListener("input", expandInputField);

h1Input.addEventListener("focusin", showDeleteButtonOnFocusIn);
h1Input.addEventListener("focusout", hideDeleteButtonOnFocusOut);
// EVENT LISTENER FOR BUTTON THAT ADDS NEW ELEMENT
for(let i = 0; i< newElementOptions.length; i++){
    // console.log(newElementOptions[i]);
    switch(newElementOptions[i].id){
        case "img":
            newElementOptions[i].addEventListener("click", (event) => {

            // https://developer.mozilla.org/en-US/docs/Web/API/Element/insertAdjacentElement

            let newImgUploadDiv = document.createElement("div");
            let newImgInput = document.createElement("input");
            let newImgPreview = document.createElement("img");
            let pseudoDeleteImg = document.createElement("i");
            // newImgInput.style.backgroundColor = "red";

            newImgUploadDiv.classList.add("image-div");

            let deleteImg = addClassesToElement(deleteBlock, pseudoDeleteImg);
            deleteImg.classList.remove("delete-label");
            deleteImg.classList.add("img-delete-label");
            deleteImg.style.color = "white";
            deleteImg.style.backgroundColor = "black";

            newImgUploadDiv.style.height = "400px";
            newImgUploadDiv.appendChild(newImgInput);
            newImgUploadDiv.appendChild(newImgPreview);

            newImgInput.type = "file";
            newImgInput.accept = "image/*";
            newImgInput.setAttribute("data-type", "img");

            newImgPreview.style.display = "none";
            newImgPreview.alt = "image preview";
           
            newImgInput.addEventListener("change", (event) => {
                previewImageUpload(newImgPreview, event.target, newImgUploadDiv);
            });
            deleteImg.addEventListener("click", deleteElementContainer);
            newImgUploadDiv.appendChild(deleteImg);
            // newImgUploadDiv.appendChild(newImgPreview);
            newElementSelectContainer.insertAdjacentElement("beforebegin", newImgUploadDiv);
            });
            break;

        case "h2":
            newElementOptions[i].addEventListener("click", (event) => {
               let newHeadingUploadDiv = document.createElement("div");
               let newH2 =  document.createElement("input");
               let pseudoDeleteLabel = document.createElement("i");

               newHeadingUploadDiv.classList.add("h2-div");
               newH2.classList.add("new-h2-elements-input");
               newH2.setAttribute("data-type", "h2");
               let deleteLabel = addClassesToElement(deleteBlock, pseudoDeleteLabel);

               newH2.addEventListener("focusout", removeBorder);
               newH2.addEventListener("input", expandInputField);
               deleteLabel.addEventListener("click", deleteElementContainer);

               newHeadingUploadDiv.appendChild(newH2);
               newHeadingUploadDiv.appendChild(deleteLabel);
               newH2.addEventListener("focusout", hideDeleteButtonOnFocusOut);
                newH2.addEventListener("focusin", showDeleteButtonOnFocusIn);
               
               newElementSelectContainer.insertAdjacentElement("beforebegin", newHeadingUploadDiv);
            });
            break;
        
        case "p":
            
            newElementOptions[i].addEventListener("click", (event) => {
               let newParagraphUploadDiv = document.createElement("div");
               let newP =  document.createElement("input");
               let pseudoDeleteLabel = document.createElement("i");

               newParagraphUploadDiv.classList.add("p-div");
               newP.classList.add("new-p-elements-input");
               newP.setAttribute("data-type", "p");
               let deleteLabel = addClassesToElement(deleteBlock, pseudoDeleteLabel);

               newP.addEventListener("input", expandInputField);
               newP.addEventListener("focusout", removeBorder);
               deleteLabel.addEventListener("click", deleteElementContainer);

               newParagraphUploadDiv.appendChild(newP);
               newParagraphUploadDiv.appendChild(deleteLabel);
               newP.addEventListener("focusout", hideDeleteButtonOnFocusOut);
                newP.addEventListener("focusin", showDeleteButtonOnFocusIn);
               newElementSelectContainer.insertAdjacentElement("beforebegin", newParagraphUploadDiv);
            });
            break;

        case "ul":
            
            newElementOptions[i].addEventListener("click", (event) => {
                let listDiv = document.createElement("div");
                let ulistItem = document.createElement("ul");

                let listItem = document.createElement("li");
                let pseudoDeleteLabel = document.createElement("i");
                let deleteLabel = addClassesToElement(deleteBlock, pseudoDeleteLabel);
                let savingToInput = document.createElement("input");

                // make list content editable && append to div
                listItem.contentEditable = "true";
                listItem.classList.add("remove-borders");

                savingToInput.style.display = "none";
                // savingToInput.name = "list";
                savingToInput.setAttribute("data-type", "ul");

                listItem.focus();
                listDiv.classList.add("ul-div")
                listDiv.appendChild(savingToInput);
                listDiv.appendChild(ulistItem);
                listDiv.appendChild(deleteLabel);
                // listDiv.addEventListener("focusout", hideDeleteButtonOnFocusOut)

                ulistItem.appendChild(listItem);

                deleteLabel.addEventListener("click", deleteElementContainer);

                listItem.addEventListener("keydown", (event) => {
                    // 
                    createListItems(event, ulistItem, savingToInput);
                    // console.log(savingToInput.value);
                });
                ulistItem.addEventListener("focusout", hideDeleteButtonOnFocusOut);
                ulistItem.addEventListener("focusin", showDeleteButtonOnFocusIn);
                // listItem.addEventListener("onfocusout")
                
                newElementSelectContainer.insertAdjacentElement("beforebegin", listDiv);
            });
            break;
    }
}

// ----------------------------------------------------------------------------------------------------------------------------------
// ///ALL FUNCTIONS BELOW

function hideDeleteButtonOnFocusOut(event){
    // console.log(event.currentTarget.parentElement);
    
    let divDeleteLabel = event.currentTarget.parentElement.querySelector(".delete-label");
    // console.log(divDeleteLabel);
    divDeleteLabel.style.visibility = "hidden";
}
function showDeleteButtonOnFocusIn(event){
    console.log(event.currentTarget);
    let divDeleteLabel = event.currentTarget.parentElement.querySelector(".delete-label");
    console.log(divDeleteLabel);
    divDeleteLabel.style.visibility = "visible";
}
function createListItems(event, ulContainer, hiddenInput){
   
    if(event.key === "Enter"){
        event.preventDefault();
        let newListItem = document.createElement("li");
        newListItem.contentEditable = "true";
        newListItem.classList.add("remove-borders");
        ulContainer.appendChild(newListItem);
        console.log(newListItem.innerText.length);
        newListItem.innerText.trim();
        newListItem.addEventListener("keydown", (event) => {
            createListItems(event, ulContainer, hiddenInput);
            // console.log(hiddenInput.value);
        });
        newListItem.focus()
        // hiddenInput.value += event.target.innerText + "\n";

    }else if(event.key === "Backspace" || event.key === "Delete"){
        console.log(event.target.innerText.length);
        
        if(event.target.innerText.length <= 1){

            if(event.target.parentElement.childElementCount < 2){
                event.target.parentElement.parentElement.remove();
                return;
            }
            event.target.remove();
        }
    }
}

function addClassesToElement(fromElement, toElement){
    for(let i = 0; i < fromElement.classList.length; i++){
        toElement.classList.add(fromElement.classList[i]);
    }
    return toElement;
}

function removeBorder(event){
//console.log("border remove")
        if(event.target.value.trim().length > 0){
            // console.log("condition");
            event.target.classList.add("remove-borders");
        }else{
            if(event.target.classList.contains("remove-borders")){
                event.target.classList.remove("remove-borders"); 
            }
        }
}

function createTextArea(externalEvent){
    let inputAttributes = externalEvent.target.attributes;
            // console.log(inputFieldExpand[i].value);
    let textArea = document.createElement("textarea");

    for (const attr of inputAttributes) {
        textArea.setAttribute(attr.name, attr.value);
        // console.log(textArea);
    }
    
    textArea.setAttribute("rows", "2");
    textArea.value = externalEvent.target.value;
    textArea.setAttribute("value", externalEvent.target.value);
    return textArea;
}

function expandInputField(event){
    if(event.target.scrollWidth > event.target.clientWidth){// CHECK IT SCROLL WIDTH HIGHER THAN CLIENT SCREEN ELEMENT WIDTH TO CHANGE TO TEXTAREA;
        let newTextArea = createTextArea(event);

        newTextArea.addEventListener("input", increaseTextAreaHeight);
        newTextArea.addEventListener("keydown", backspaceDeleteRowsTextArea);
        newTextArea.addEventListener("focusout", removeBorder);
        event.target.replaceWith(newTextArea);
        newTextArea.focus();
        const rect = newTextArea.getBoundingClientRect();
        simulated_event = {
            target: newTextArea,
        };
        increaseTextAreaHeight(simulated_event);
    }
}

function increaseTextAreaHeight(event){
//    console.log(event.target.scrollHeight, event.target.clientHeight);
    if(event.target.scrollHeight > event.target.clientHeight){
        // my original solution
        let rowSize = parseInt(event.target.getAttribute("rows")) + 1;
        // console.log(textArea.getAttribute("rows"), rowSize);
        event.target.rows = `${rowSize}`;
        event.target.setAttribute("rows", `${rowSize}`);
        increaseTextAreaHeight(event);
//           dont really know why this works, but it works....
//            event.target.dispatchEvent(new Event('input', { 'bubbles': true }))

//        online solution
//        event.target.style.height = '0';
//
//        event.target.style.height = (textarea.scrollHeight + 16) + 'px'

    }
}

function backspaceDeleteRowsTextArea(event){
    if(event.key === "Backspace" || event.key === "Delete"){
        const rect = event.target.getBoundingClientRect();
        if(event.target.value[event.target.value.length - 1] == "\n" ){
            let currentTextRows = event.target.rows;
            let newTextRows = parseInt(currentTextRows) - 1;
            event.target.setAttribute("rows", `${newTextRows}`);
            // if(event.target.clientHeight > event.target.scrollHeight){
            //     console.log("called:", event.target.clientHeight, event.target.scrollHeight);
            //     backspaceDeleteRowsTextArea(event);
            // }
        }else if(event.target.value.trim().length < 1){
            deleteElementContainer(event);
        }
    }
}

function previewImageUpload(previewElement, inputElement, container){
    // my solution based on MDN Docs..
    // console.log(this.files, this.files[0].size); for the input element
    console.log(previewElement);
    previewElement.style.display = "block";
    previewElement.src = URL.createObjectURL(inputElement.files[0]);
    container.style.height = "auto";
}

function deleteElementContainer(event){
    console.log(event);
        // console.log(deleteBlock[i].parentElement.children[0]);
    if(event.target.parentElement.querySelector('.title-input')){
        alert("can't have an article without a title man🙄🙄")
        return;
    }
    event.target.parentElement.remove();
}
