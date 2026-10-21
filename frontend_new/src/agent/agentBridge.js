export function getPageElements() {
    const elements = []
    document.querySelectorAll('[data-agent]').forEach(el => {
        /** @type {HTMLElement} */
        const htmlEl = (el)
        const element_metadata = htmlEl.getBoundingClientRect()
        elements.push({
            id: htmlEl.getAttribute("data-agent"),
            tag: htmlEl.tagName.toLowerCase(),
            text: htmlEl.innerText?.trim() || htmlEl.getAttribute("placeholder") || "",
            type: htmlEl.getAttribute("type"),
            x: Math.round(element_metadata.x + element_metadata.width / 2),
            y: Math.round(element_metadata.y + element_metadata.height / 2)
        })
    })
    return elements
}

/**
 * Receives a single action from the backend and executes it on the live DOM.
 * Called by AgentChat.jsx once per action in the actions array,
 * with a small delay between each so the user can see each step.
 *
 * @param {{ type: string, id: string, text?: string, key?: string }} action
 * @returns {{ success: boolean, error?: string }}
 */
export function executeAction(action) {
    /** @type {HTMLElement} */
    const el = (document.querySelector(`[data-agent="${action.id}"]`))
    if (!el) return {success : false, error: `Element ${action.id} not found`}

    console.log("The Agent wants this action type", action.type);

    switch(action.type){
        case "click": {
            const el = document.querySelector(`[data-agent="${action.id}"]`);
            if (!el) return { success: false };

            el.scrollIntoView({ behavior: "smooth", block: "center" });

            // force real DOM click (more reliable than MouseEvent)
            el.click();
            return new Promise(resolve => {
                setTimeout(() => {
                    resolve({ success: true });
                }, 300); // 👈 allow React to settle
            });         
        }

        case "type": {
            el.focus()

            // determine what kind of prototype the input element is
            const prototype = el.tagName.toLowerCase() === "textarea"
                ? HTMLTextAreaElement.prototype
                : HTMLInputElement.prototype
            //

            const nativeInputSetter = Object.getOwnPropertyDescriptor(
                prototype, "value"
            ).set
            nativeInputSetter.call(el, action.text ?? "")
            el.dispatchEvent(new Event("input", {bubbles: true}))
            console.log("Input TARGET:", el);
            return {success: true}
        }

        case "press_key": {
            el.dispatchEvent(new KeyboardEvent("keydown", {
                key: action.key,
                bubbles: true
            }))
            return {success: true}
        }

        case "clear":{
            el.focus();
            el.value = "";
            el.dispatchEvent(new Event("input", {bubbles: true}));
            return { success: true };
        }
        default:
            return {success: false, error: `Unknown action type: ${action.type}`}
    }

}