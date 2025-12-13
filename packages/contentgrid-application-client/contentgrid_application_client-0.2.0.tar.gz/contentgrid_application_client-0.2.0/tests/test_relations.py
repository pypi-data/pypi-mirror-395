from contentgrid_application_client import ContentGridApplicationClient, EntityCollection
from contentgrid_hal_client.exceptions import Forbidden, MissingHALTemplate
from fixtures import auth_manager, cg_client # noqa: F401
import pytest


class TestRelations:
    entity_name = "candidate"
    relation_name = "skills"

    def test_relations(self, cg_client: ContentGridApplicationClient):
        entity = cg_client.create_entity(self.entity_name, {"name": "test"})

        # fetch related skills
        related_skills = cg_client.get_entity_relation_collection(
            entity.get_self_link(), self.relation_name
        )

        assert isinstance(related_skills, EntityCollection)

        # entity just instantiated so no skills
        assert len(related_skills.get_entities()) == 0

        skills = cg_client.get_entity_collection(singular_entity_name="skill")

        amt_skills_to_sample = 4
        skills_selection = skills.get_entities()[:amt_skills_to_sample]
        assert len(skills_selection) == amt_skills_to_sample

        skills_selection[1] = skills_selection[1].get_self_link().uri
        skills_selection[2] = skills_selection[2].get_self_link()

        cg_client.post_entity_relation(
            entity.get_self_link(),
            relation_name=self.relation_name,
            related_entity_links=skills_selection[:-1],
        )

        related_skills.refetch()

        assert len(related_skills.get_entities()) == amt_skills_to_sample - 1
        
        # post last skill
        cg_client.post_entity_relation(
            entity_link=entity.get_self_link(),
            relation_name=self.relation_name,
            related_entity_links=[skills_selection[-1]],
        )

        related_skills = cg_client.get_entity_relation_collection(
            entity_link=entity.get_self_link(), relation_name=self.relation_name
        )
        assert len(related_skills.get_entities()) == amt_skills_to_sample

        entity.delete()
        
    def test_put_on_to_many_not_supported(self, cg_client: ContentGridApplicationClient):
        entity = cg_client.create_entity(self.entity_name, {"name": "test"})
        
        skills = cg_client.get_entity_collection(singular_entity_name="skill")
        skills_selection = skills.get_entities()[:2]
        
        # PUT on to-many relations should raise Forbidden
        with pytest.raises(MissingHALTemplate):
            cg_client.put_entity_relation(
                entity.get_self_link(),
                relation_name=self.relation_name,
                related_entity_links=skills_selection,
            )
        
        entity.delete()
        
    def test_clear_relations(self, cg_client: ContentGridApplicationClient):
        entity = cg_client.create_entity(self.entity_name, {"name": "test"})
        # no related exist yet
        entity.clear_relation(relation_name=self.relation_name)
        
        skills = cg_client.get_entity_collection(singular_entity_name="skill")
        skills_selection = skills.get_entities()[:1]
        cg_client.post_entity_relation(
            entity.get_self_link(),
            relation_name=self.relation_name,
            related_entity_links=skills_selection,
        )
        
        assert len(entity.get_relation_collection(relation_name=self.relation_name).get_entities()) == 1
        
        #clear relations again
        entity.clear_relation(relation_name=self.relation_name)
    
    

