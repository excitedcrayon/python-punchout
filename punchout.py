#!usr/bin/python

from tkinter import Tk, Frame, Label, Text, Button, Entry
from tkinter import ttk
import requests
import re
import xml.etree.ElementTree as ET


class Punchout(Tk):
    def __init__(self):
        super().__init__()

        self.punchout_environment_value = None

        self.window_width = 500
        self.window_height = 750

        self.widget_width = 50
        self.widget_height = 50

        self.widget_y_padding = 20

        self.widget_font = {"font": ("Calibri", 12)}
        self.widget_text_font = {"font": ("Calibri", 10)}

        self.punchout_select_options = ["", "Local", "S1 Test", "P1 Prod"]

        self.punchout_local_link = "https://cnw.local:9002/punchout/cxml/setup?site=cnw"
        self.punchout_p1_link = "https://shop.cnw.com.au/punchout/cxml/setup?site=cnw"
        self.punchout_s1_link = "https://cnw.c94gvn2mno-cnwsub3-s1-public.model-t.cc.commerce.ondemand.com/punchout/cxml/setup?site=cnw"

        self.title("Punchout Session")
        self.resizable(False, False)
        self.center_main_window()

        self.topFrame = Frame(self, pady=self.widget_y_padding)
        self.top_section_punch_out_mode()
        self.middleFrame = Frame(self)
        self.middle_section_identity_sharedsecret()
        self.bottomFrame = Frame(self)
        self.bottom_section_buttons()

    def center_main_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - self.window_width) / 2)
        y_position = int((screen_height - self.window_height) / 2)
        self.geometry(
            f"{self.window_width}x{self.window_height}+{x_position}+{y_position}"
        )

    def top_section_punch_out_mode(self):
        # Punchout Label
        self.punchout_label = Label(
            self.topFrame,
            text="Punchout Environment *",
            **self.widget_font,
        )
        self.punchout_label.pack()
        self.punchout_label.grid(row=0, column=0)

        # Punchout Select Drop down box
        self.punchout_select = ttk.Combobox(
            self.topFrame,
            width=self.widget_width - 3,
            values=self.punchout_select_options,
            **self.widget_font,
        )
        self.punchout_select.bind(
            "<<ComboboxSelected>>",
            lambda event: self.set_environment_value(self.punchout_select.get()),
        )
        self.punchout_select.grid(row=1, column=0, pady=self.widget_y_padding / 5)
        self.punchout_select.current(0)
        self.punchout_select.set(self.punchout_select_options[0])

        self.topFrame.pack()

    def middle_section_identity_sharedsecret(self):
        # Identity Label
        self.punchout_identity_label = Label(
            self.middleFrame,
            text="Identity *",
            width=self.widget_width,
            **self.widget_font,
        )

        self.punchout_identity_label.grid(row=0, column=0)

        # Identity Entry Field
        self.punchout_identity_entry = Entry(
            self.middleFrame, width=self.widget_width, **self.widget_font
        )
        self.punchout_identity_entry.grid(
            row=1, column=0, pady=self.widget_y_padding / 4
        )
        self.punchout_identity_value = self.punchout_identity_entry.get()
        print(self.punchout_identity_entry.get())

        # Shared Secret Label
        self.punchout_sharedsecret_label = Label(
            self.middleFrame,
            text="Shared Secret *",
            **self.widget_font,
        )
        self.punchout_sharedsecret_label.grid(row=2, column=0)

        # Shared Secret Entry Field
        self.punchout_sharedsecret_entry = Entry(
            self.middleFrame, width=self.widget_width, **self.widget_font
        )
        self.punchout_sharedsecret_entry.grid(
            row=3, column=0, pady=self.widget_y_padding / 4
        )

        # Session Link Label
        self.punchout_session_label = Label(
            self.middleFrame, text="Session Link", **self.widget_font
        )
        self.punchout_session_label.grid(row=4, column=0, pady=self.widget_y_padding)

        # Session Link Textbox
        self.punchout_session_text = Text(
            self.middleFrame,
            width=self.widget_width,
            height=20,
            pady=self.widget_y_padding,
            bg="black",
            fg="white",
        )
        self.punchout_session_text.grid(row=5, column=0)

        self.middleFrame.pack()

    def bottom_section_buttons(self):
        # Generate Button
        self.generate_button = Button(
            self.bottomFrame,
            text="Generate Session Link",
            command=self.generate_session_link,
        )
        self.generate_button.grid(row=0, column=0, pady=self.widget_y_padding)

        # Clear Textbox Button
        self.clear_text_box = Button(
            self.bottomFrame,
            text="Clear Session",
            command=self.clear_session,
        )
        self.clear_text_box.grid(row=0, column=1, pady=self.widget_y_padding)

        # Close Button
        self.exit = Button(self.bottomFrame, text="Exit", command=self.close_window)
        self.exit.grid(row=0, column=2, pady=self.widget_y_padding)

        self.bottomFrame.pack()

    def generate_session_link(self):
        environment = self.get_environmental_value()
        identity = self.get_identity_value()
        shared_secret = self.get_shared_secret()

        url_link = self.api_post_link(environment)
        string_xml_data = self.xml_string_raw_data(
            identity=identity, shared_secret=shared_secret
        )
        xml_data = string_xml_data.encode("UTF-8")
        headers = {"Content-Type": "application/xml"}

        if (
            environment != "Local"
            or environment != "S1 Test"
            or environment != "P1 Prod"
        ):
            self.punchout_session_text.insert(
                "1.0", "[Error] Please select environment!"
            )
        if (
            environment == "Local"
            or environment == "S1 Test"
            or environment == "P1 Prod"
        ):
            # send the data as bytes
            response = requests.post(url_link, headers=headers, data=xml_data).text
            status_code = self.get_status_code_from_response(response)

            # populate session output Text widget
            self.punchout_session_text.delete("1.0", "end")
            self.punchout_session_text.insert("1.0", f"[Link] {url_link}\n\n")
            self.punchout_session_text.insert(
                "2.0", "[Process] Requesting Punchout Session Link...........\n\n"
            )
            self.punchout_session_text.insert("3.0", "\n")
            self.punchout_session_text.insert("5.0", "[Response]\n" + str(response))

    def clear_session(self):
        self.punchout_session_text.delete("1.0", "end")

    def close_window(self):
        self.destroy()

    def api_post_link(self, option_value) -> str:
        post_link = ""
        match option_value:
            case "Local":
                post_link = self.punchout_local_link
            case "S1 Test":
                post_link = self.punchout_s1_link
            case "P1 Prod":
                post_link = self.punchout_p1_link
            case _:
                """"""
        return post_link

    def xml_string_raw_data(self, identity, shared_secret) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
            <cXML payloadID="1645478194.5713@punchoutcommerce.com" timestamp="2022-02-21T21:16:34+00:00">
              <Header>
                <From>
                  <Credential domain="NetworkId">
                    <Identity>{identity}</Identity>
                  </Credential>
                </From>
                <To>
                  <Credential domain="DUNS">
                    <Identity>sysadmin@ariba.com</Identity>
                  </Credential>
                </To>
                <Sender>
                  <Credential domain="NetworkId">
                    <Identity>{identity}</Identity>
                    <SharedSecret>{shared_secret}</SharedSecret>
                  </Credential>
                  <UserAgent>PunchOutCommerce PunchOut Tester</UserAgent>
                </Sender>
              </Header>
              <Request deploymentMode="production">
                <PunchOutSetupRequest operation="create">
                  <BuyerCookie>4ee4881052f2926059c57c6b23abd8e9</BuyerCookie>
                  <Extrinsic name="User">jdoe12345</Extrinsic>
                  <Extrinsic name="UniqueUsername">jdoe12345</Extrinsic>
                  <Extrinsic name="UserId">12345</Extrinsic>
                  <Extrinsic name="UserEmail">jdoe@example.com</Extrinsic>
                  <Extrinsic name="UserFullName">John Doe</Extrinsic>
                  <Extrinsic name="UserPrintableName">John Doe</Extrinsic>
                  <Extrinsic name="FirstName">John</Extrinsic>
                  <Extrinsic name="LastName">Doe</Extrinsic>
                  <Extrinsic name="PhoneNumber">555-555-5555</Extrinsic>
                  <BrowserFormPost>
                   <URL>https://punchoutcommerce.com/tools/cxml-punchout-return</URL>
                  </BrowserFormPost>
                  <SupplierSetup>   
                    <URL>https://cnw.c94gvn2mno-cnwsub3-s1-public.model-t.cc.commerce.ondemand.com/punchout/cxml/setup?site=cnw</URL>
                  </SupplierSetup>
                  <ShipTo>
                    <Address addressID="TEST">
                      <Name xml:lang="en">TEST</Name>
                      <PostalAddress>
                        <Street>123 Street Address</Street>
                        <City>Rockville</City>
                        <State>MD</State>
                        <PostalCode>20850</PostalCode>
                        <Country isoCountryCode="US">US</Country>
                      </PostalAddress>
                    </Address>
                  </ShipTo>
                </PunchOutSetupRequest>
              </Request>
            </cXML>
        """

    def set_environment_value(self, environment_value):
        self.punchout_environment_value = environment_value

    def get_environmental_value(self) -> str:
        return str(self.punchout_environment_value)

    def get_identity_value(self) -> str:
        return str(self.punchout_identity_entry.get())

    def get_shared_secret(self) -> str:
        return str(self.punchout_sharedsecret_entry.get())

    def get_status_code_from_response(self, response) -> str:
        convert_from_string = ET.fromstring(response)
        convert_to_bytes = ET.tostring(convert_from_string)
        string_from_bytes = convert_to_bytes.decode("UTF-8")
        print(type(string_from_bytes))
        print(string_from_bytes)


if __name__ == "__main__":
    punchout = Punchout()
    punchout.mainloop()
