# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""
Streaming provider wrapper classes for Featureform.
"""

from typing import TYPE_CHECKING, List, Optional, Union

from ..resources import StreamChannel

if TYPE_CHECKING:
    from ..registrar import UserRegistrar

from .offline import OfflineProvider

__all__ = ["KafkaProvider"]


class KafkaProvider(OfflineProvider):
    def __init__(self, registrar, provider):
        super().__init__(registrar, provider)
        self.__registrar = registrar
        self.__provider = provider

    def register_kafka_topic(
        self,
        name: str,
        topic: str,
        description: str = "",
        tags: Optional[List[str]] = None,
        properties: Optional[dict] = None,
        owner: Union[str, "UserRegistrar"] = "",
    ):
        """Register a Kafka topic as a primary data source.

        **Examples**

        ```
        spark = client.get_provider("my_spark")
        transactions_stream = spark.register_kafka_topic(
            name="transactions_stream",
            topic="transactions",
            description="A stream of transaction data from Kafka"
        )
        ```

        Args:
            name (str): Name to register the Kafka topic under.
            topic (str): The name of the Kafka topic.
            variant (str, optional): Variant name, if applicable.
            owner (Union[str, "UserRegistrar"], optional): Owner of the data source.
            description (str, optional): Description of the Kafka topic.
            tags (List[str], optional): Tags associated with the data source.
            properties (dict, optional): Additional properties.

        Returns:
            source (ColumnSourceRegistrar): The registered data source.
        """

        tags, properties = set_tags_properties(tags, properties)

        topic = StreamChannel(
            name=name,
            channel_name=topic,
            provider=self.name(),
            owner=owner,
            description=description,
        )
        self.__registrar.add_resource(topic)
        return topic
