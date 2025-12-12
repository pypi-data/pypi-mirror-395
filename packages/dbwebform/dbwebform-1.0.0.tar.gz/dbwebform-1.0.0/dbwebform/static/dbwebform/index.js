"use strict";
const form = document.querySelector('.form');
const script = document.currentScript;
const notification_text = script.dataset.notificationText || null, method = script.dataset.method || "GET";
input_form_control_unline(form);
formInputReversed(form);
if (notification_text && method === "POST") {
    const notification = new HyperTextNotification({ backgroundColor: 'rgba(192,0,192,0.8)' });
    notification.show(notification_text);
}
//# sourceMappingURL=index.js.map