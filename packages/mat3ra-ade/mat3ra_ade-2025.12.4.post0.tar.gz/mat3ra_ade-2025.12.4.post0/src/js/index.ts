import Application from "./application";
import { applicationMixin, applicationStaticMixin } from "./applicationMixin";
import ApplicationRegistry from "./ApplicationRegistry";
import ContextProvider from "./context/ContextProvider";
import JSONSchemaFormDataProvider from "./context/JSONSchemaFormDataProvider";
import Executable from "./executable";
import { executableMixin } from "./executableMixin";
import Flavor from "./flavor";
import { flavorMixin } from "./flavorMixin";
import Template from "./template";
import { templateMixin, templateStaticMixin } from "./templateMixin";

const allApplications = ApplicationRegistry.getUniqueAvailableApplicationNames();

export {
    Application,
    Executable,
    Flavor,
    Template,
    ApplicationRegistry,
    ContextProvider,
    JSONSchemaFormDataProvider,
    executableMixin,
    flavorMixin,
    applicationMixin,
    applicationStaticMixin,
    templateMixin,
    templateStaticMixin,
    allApplications,
};

export type * from "./types";
