from dataclasses import dataclass, asdict
from enum import Enum, auto
import json
from typing import List


class ContributorType(Enum):
    ContactPerson         =auto()
    DataCollector         =auto()
    DataCurator           =auto()
    DataManager           =auto()
    Distributor           =auto()
    Editor                =auto()
    HostingInstitution    =auto()
    Other                 =auto()
    Producer              =auto()
    ProjectLeader         =auto()
    ProjectManager        =auto()
    ProjectMember         =auto()
    RegistrationAgency    =auto()
    RegistrationAuthority =auto()
    RelatedPerson         =auto()
    ResearchGroup         =auto()
    Researcher            =auto()
    RightsHolder          =auto()
    Sponsor               =auto()
    Supervisor            =auto()
    WorkPackageLeader     =auto()

    @property
    def label(self):
        return self.name

class Relation(Enum):
    isCitedBy             =auto()
    cites                 =auto()
    isSupplementTo        =auto()
    isSupplementedBy      =auto()
    references            =auto()
    isReferencedBy        =auto()
    isPublishedIn         =auto()
    isNewVersionOf        =auto()
    isPreviousVersionOf   =auto()
    isContinuedBy         =auto()
    continues             =auto()
    isDescribedBy         =auto()
    describes             =auto()
    isPartOf              =auto()
    hasPart               =auto()
    isReviewedBy          =auto()
    reviews               =auto()
    isDocumentedBy        =auto()
    documents             =auto()
    compiles              =auto()
    isCompiledBy          =auto()
    isDerivedFrom         =auto()
    isSourceOf            =auto()
    requires              =auto()
    isRequiredBy          =auto()
    isObsoletedBy         =auto()
    obsoletes             =auto()
    isIdenticalTo         =auto()
    isAlternateIdentifier =auto()

    @property
    def label(self):
        return self.name

class ResourceType(Enum):
    publication                       =auto()
    publication_annotationcollection  =auto()
    publication_book                  =auto()
    publication_section               =auto()
    publication_conferencepaper       =auto()
    publication_datamanagementplan    =auto()
    publication_article               =auto()
    publication_other                 =auto()
    publication_patent                =auto()
    publication_preprint              =auto()
    publication_deliverable           =auto()
    publication_milestone             =auto()
    publication_proposal              =auto()
    publication_report                =auto()
    publication_softwaredocumentation =auto()
    publication_taxonomictreatment    =auto()
    publication_technicalnote         =auto()
    publication_thesis                =auto()
    publication_workingpaper          =auto()
    dataset                           =auto()
    image                             =auto()
    image_diagram                     =auto()
    image_drawing                     =auto()
    image_figure                      =auto()
    image_other                       =auto()
    image_photo                       =auto()
    image_plot                        =auto()
    lesson                            =auto()
    other                             =auto()
    physicalobject                    =auto()
    poster                            =auto()
    presentation                      =auto()
    software                          =auto()
    video                             =auto()
    workflow                          =auto()

    @property
    def label(self):
        return self.name.replace('_', '-')

class UploadType(Enum):
    publication    =auto()
    dataset        =auto()
    image          =auto()
    lesson         =auto()
    other          =auto()
    physicalobject =auto()
    poster         =auto()
    presentation   =auto()
    software       =auto()
    video          =auto()
    workflow       =auto()

    @property
    def label(self):
        return self.name


@dataclass
class Contributor():
    name                :str
    affiliation         :str
    orcid               :str             =None
    type                :ContributorType =ContributorType.DataCollector


@dataclass
class Creator():
    name                :str
    affiliation         :str


@dataclass
class Identifier():
    identifier          :str
    relation            :Relation
    resource_type       :ResourceType =None
    scheme              :str          =None  # set by Zenodo


@dataclass
class Subject():
    term                :str
    identifier          :str        # e.g., https://some.url/id
    scheme              :str =None  # set by Zenodo


@dataclass
class MetaData():
    title               :str
    description         :str
    upload_type         :UploadType        =UploadType.dataset  # fixed
    access_right        :str               =None
    contributors        :List[Contributor] =None
    creators            :List[Creator]     =None
    doi                 :str               =None
    keywords            :List[str]         =None
    language            :str               =None
    license             :str               =None
    notes               :str               =None
    publication_date    :str               =None
    related_identifiers :List[Identifier]  =None
    subjects            :List[Subject]     =None
    version             :str               =None

    def to_json(self):
        sparse_dict = {
            x: [{
                    xx:yy.label if isinstance(yy, Enum) else yy
                    for xx,yy in i.items()
                    if yy is not None
                } if isinstance(i, dict) else i
                for i in y
            ] if isinstance(y, list) else y.label if isinstance(y, Enum) else y
            for x,y in asdict(self).items()
            if y is not None
        }
        return json.dumps({"metadata": sparse_dict})
